#!/usr/bin/env node

const inquirer = require('inquirer');
const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const Table = require('cli-table3');
const ora = require('ora');
const cliProgress = require('cli-progress');
const cliCursor = require('cli-cursor');

const { convertToMp3, calculateBitrate } = require('./convert');

class VisualConverter {
  constructor() {
    this.spinner = null;
    this.progressBar = null;
  }

  // Show welcome banner
  showWelcome() {
    console.clear();
    console.log(chalk.bold.blue(`
╔══════════════════════════════════════════════════════════════╗
║                 🎵 M4A to MP3 Converter v2.0                 ║
║                   with Interactive CLI                       ║
╚══════════════════════════════════════════════════════════════╝
`));
  }

  // Show file table
  async showFileTable(files) {
    if (files.length === 0) {
      console.log(chalk.yellow('📁 No M4A files found in the input directory.'));
      return [];
    }

    const table = new Table({
      head: [
        chalk.cyan('Index'),
        chalk.cyan('Filename'),
        chalk.cyan('Size'),
        chalk.cyan('Duration'),
        chalk.cyan('Estimated MP3')
      ],
      style: {
        head: [],
        border: ['cyan']
      }
    });

    const fileDetails = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const stats = await fs.stat(file);
      const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);

      // Get duration (simplified - in real implementation would use ffprobe)
      const duration = 'Calculating...';

      // Estimate MP3 size (rough calculation)
      const estimatedMp3MB = Math.min(sizeMB * 0.3, 15).toFixed(2);

      table.push([
        chalk.yellow(i + 1),
        chalk.white(path.basename(file)),
        chalk.red(`${sizeMB}MB`),
        chalk.blue(duration),
        chalk.green(`~${estimatedMp3MB}MB`)
      ]);

      fileDetails.push({
        index: i + 1,
        file: file,
        filename: path.basename(file),
        size: parseFloat(sizeMB),
        estimatedOutput: parseFloat(estimatedMp3MB)
      });
    }

    console.log(chalk.bold('\n📋 Available M4A Files:\n'));
    console.log(table.toString());

    return fileDetails;
  }

  // Interactive file selection menu
  async selectFiles(fileDetails) {
    if (fileDetails.length === 0) return [];

    const choices = [
      {
        name: chalk.green('✅ Convert ALL files'),
        value: 'all',
        short: 'All files'
      },
      {
        name: chalk.yellow('📂 Select specific files'),
        value: 'select',
        short: 'Select files'
      },
      {
        name: chalk.red('❌ Cancel'),
        value: 'cancel',
        short: 'Cancel'
      }
    ];

    const { selection } = await inquirer.prompt([
      {
        type: 'list',
        name: 'selection',
        message: chalk.bold('What would you like to do?'),
        choices: choices,
        pageSize: 10
      }
    ]);

    if (selection === 'cancel') return [];
    if (selection === 'all') return fileDetails;

    // Multi-select specific files
    const fileChoices = fileDetails.map(detail => ({
      name: `${chalk.yellow(detail.index)}. ${detail.filename} (${chalk.red(detail.size + 'MB')} → ${chalk.green('~' + detail.estimatedOutput + 'MB')})`,
      value: detail,
      short: detail.filename
    }));

    const { selectedFiles } = await inquirer.prompt([
      {
        type: 'checkbox',
        name: 'selectedFiles',
        message: chalk.bold('Select files to convert:'),
        choices: fileChoices,
        pageSize: 15,
        validate: (answer) => {
          if (answer.length === 0) {
            return chalk.red('Please select at least one file.');
          }
          return true;
        }
      }
    ]);

    return selectedFiles;
  }

  // Show conversion settings
  async confirmSettings(selectedFiles, outputDir) {
    const totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0);
    const estimatedTotalOutput = selectedFiles.reduce((sum, file) => sum + file.estimatedOutput, 0);

    console.log(chalk.bold('\n⚙️  Conversion Settings:\n'));
    console.log(`📁 Output Directory: ${chalk.cyan(outputDir)}`);
    console.log(`📊 Files Selected: ${chalk.yellow(selectedFiles.length)}`);
    console.log(`📏 Total Input Size: ${chalk.red(totalSize.toFixed(2) + 'MB')}`);
    console.log(`🎯 Estimated Output: ${chalk.green(estimatedTotalOutput.toFixed(2) + 'MB')}`);
    console.log(`🗜️  Target Size Limit: ${chalk.blue('16MB per file')}`);

    const { confirm } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirm',
        message: chalk.bold('Start conversion?'),
        default: true
      }
    ]);

    return confirm;
  }

  // Convert files with visual progress
  async convertFiles(selectedFiles, outputDir) {
    console.log(chalk.bold('\n🚀 Starting Conversion...\n'));

    const results = [];
    let completed = 0;

    // Main progress bar for overall conversion
    const mainProgress = new cliProgress.MultiBar({
      format: chalk.cyan('{bar}') + ' {percentage}% | ETA: {eta}s | {value}/{total} files',
      barCompleteChar: '\u2588',
      barIncompleteChar: '\u2591',
      hideCursor: true
    });

    const overallBar = mainProgress.create(selectedFiles.length, 0, { task: 'Overall Progress' });

    for (const fileDetail of selectedFiles) {
      const inputPath = fileDetail.file;
      const outputPath = path.join(outputDir, fileDetail.filename.replace('.m4a', '.mp3'));

      console.log(chalk.bold(`\n📀 Converting: ${chalk.cyan(fileDetail.filename)}`));

      // File-specific progress bar
      const fileBar = mainProgress.create(100, 0, {
        task: `Converting ${fileDetail.filename}`,
        filename: fileDetail.filename
      });

      try {
        // Create a conversion promise with progress tracking
        const result = await this.convertWithProgress(inputPath, outputPath, fileBar);

        // Update progress bars
        fileBar.update(100);
        completed++;
        overallBar.update(completed);

        // Show result
        const outputStats = await fs.stat(outputPath);
        const outputSizeMB = (outputStats.size / (1024 * 1024)).toFixed(2);
        const status = outputStats.size > 16 * 1024 * 1024 ? chalk.red('⚠️  OVER LIMIT') : chalk.green('✅ OK');

        console.log(`${chalk.green('✓')} ${fileDetail.filename}: ${chalk.blue(outputSizeMB + 'MB')} ${status}`);

        results.push({
          ...result,
          filename: fileDetail.filename,
          outputSize: outputStats.size
        });

      } catch (error) {
        console.log(`${chalk.red('✗')} ${fileDetail.filename}: ${chalk.red(error.message)}`);
        fileBar.stop();
      }

      fileBar.stop();
    }

    mainProgress.stop();
    return results;
  }

  // Convert single file with progress tracking
  convertWithProgress(inputPath, outputPath, progressBar) {
    return new Promise((resolve, reject) => {
      const ffmpeg = require('fluent-ffmpeg');
      const fs = require('fs');

      // Get file stats for duration calculation
      fs.stat(inputPath, (err, stats) => {
        if (err) {
          reject(err);
          return;
        }

        const fileSize = stats.size;

        ffmpeg(inputPath)
          .toFormat('mp3')
          .audioBitrate(128) // Will be dynamically adjusted
          .audioChannels(2)
          .audioFrequency(44100)
          .on('progress', (progress) => {
            if (progress.percent) {
              progressBar.update(Math.round(progress.percent));
            }
          })
          .on('end', async () => {
            try {
              const outputStats = await fs.promises.stat(outputPath);
              resolve({
                input: inputPath,
                output: outputPath,
                size: outputStats.size
              });
            } catch (error) {
              reject(error);
            }
          })
          .on('error', (err) => {
            reject(err);
          })
          .save(outputPath);
      });
    });
  }

  // Show conversion summary
  showSummary(results) {
    if (results.length === 0) {
      console.log(chalk.yellow('\n📊 No files were successfully converted.'));
      return;
    }

    console.log(chalk.bold('\n' + '='.repeat(60)));
    console.log(chalk.bold('🎉 CONVERSION SUMMARY'));
    console.log(chalk.bold('='.repeat(60)));

    const table = new Table({
      head: [
        chalk.cyan('File'),
        chalk.cyan('Original Size'),
        chalk.cyan('Converted Size'),
        chalk.cyan('Compression'),
        chalk.cyan('Status')
      ],
      style: {
        head: [],
        border: ['cyan']
      }
    });

    let totalOriginal = 0;
    let totalConverted = 0;

    results.forEach(result => {
      const originalSize = result.size || 0;
      const convertedSize = result.outputSize || 0;
      const compressionRatio = originalSize > 0 ? ((1 - convertedSize / originalSize) * 100).toFixed(1) : '0.0';

      const originalMB = (originalSize / (1024 * 1024)).toFixed(2);
      const convertedMB = (convertedSize / (1024 * 1024)).toFixed(2);
      const status = convertedSize > 16 * 1024 * 1024 ? chalk.red('⚠️  OVER LIMIT') : chalk.green('✅ OK');

      table.push([
        chalk.white(result.filename),
        chalk.red(originalMB + 'MB'),
        chalk.blue(convertedMB + 'MB'),
        chalk.yellow(compressionRatio + '%'),
        status
      ]);

      totalOriginal += originalSize;
      totalConverted += convertedSize;
    });

    console.log(table.toString());

    const totalOriginalMB = (totalOriginal / (1024 * 1024)).toFixed(2);
    const totalConvertedMB = (totalConverted / (1024 * 1024)).toFixed(2);
    const totalCompression = totalOriginal > 0 ? ((1 - totalConverted / totalOriginal) * 100).toFixed(1) : '0.0';

    console.log(chalk.bold('\n📈 OVERALL STATISTICS:'));
    console.log(`📊 Total Files: ${chalk.yellow(results.length)}`);
    console.log(`📏 Original Size: ${chalk.red(totalOriginalMB + 'MB')}`);
    console.log(`📏 Converted Size: ${chalk.blue(totalConvertedMB + 'MB')}`);
    console.log(`🗜️  Total Compression: ${chalk.green(totalCompression + '%')}`);
  }

  // Main menu loop
  async run() {
    while (true) {
      this.showWelcome();

      // Check for input files
      const inputDir = './input';
      if (!await fs.pathExists(inputDir)) {
        console.log(chalk.yellow('📁 Input directory not found. Creating it...'));
        await fs.ensureDir(inputDir);
      }

      const files = await this.getM4aFiles(inputDir);
      const fileDetails = await this.showFileTable(files);

      if (fileDetails.length === 0) {
        console.log(chalk.yellow('\n💡 Place your .m4a files in the input/ directory and run this command again.'));
        console.log(chalk.gray('   Press Ctrl+C to exit\n'));

        // Wait for user input or exit
        const { action } = await inquirer.prompt([
          {
            type: 'list',
            name: 'action',
            message: chalk.bold('What would you like to do?'),
            choices: [
              { name: chalk.green('🔄 Check again for files'), value: 'retry' },
              { name: chalk.red('❌ Exit'), value: 'exit' }
            ]
          }
        ]);

        if (action === 'exit') break;
        continue;
      }

      // Select files
      const selectedFiles = await this.selectFiles(fileDetails);
      if (selectedFiles.length === 0) {
        console.log(chalk.yellow('\n👋 No files selected. Goodbye!'));
        break;
      }

      // Confirm settings
      const outputDir = './output';
      await fs.ensureDir(outputDir);

      const confirmed = await this.confirmSettings(selectedFiles, outputDir);
      if (!confirmed) {
        console.log(chalk.yellow('\n👋 Conversion cancelled. Goodbye!'));
        break;
      }

      // Convert files
      const results = await this.convertFiles(selectedFiles, outputDir);

      // Show summary
      this.showSummary(results);

      // Ask to continue
      const { continue: shouldContinue } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'continue',
          message: chalk.bold('\n🔄 Convert more files?'),
          default: false
        }
      ]);

      if (!shouldContinue) break;
    }
  }

  // Get M4A files from directory
  async getM4aFiles(directory) {
    try {
      const files = await fs.readdir(directory);
      return files
        .filter(file => path.extname(file).toLowerCase() === '.m4a')
        .map(file => path.join(directory, file));
    } catch (error) {
      return [];
    }
  }
}

// Run the interactive converter
if (require.main === module) {
  const converter = new VisualConverter();
  converter.run().catch(console.error);
}

module.exports = VisualConverter;
