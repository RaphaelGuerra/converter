#!/usr/bin/env node

const ffmpeg = require('fluent-ffmpeg');
const fs = require('fs-extra');
const path = require('path');
const { promisify } = require('util');
const chalk = require('chalk');
const cliProgress = require('cli-progress');
const ora = require('ora');

const stat = promisify(fs.stat);
const readdir = promisify(fs.readdir);

// Configuration
const MAX_FILE_SIZE_MB = 16;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
const DEFAULT_BITRATE = 128; // kbps

// Calculate optimal bitrate based on estimated duration and target size
function calculateBitrate(estimatedDurationSeconds, targetSizeBytes = MAX_FILE_SIZE_BYTES) {
  // MP3 bitrate calculation: bytes = (bitrate * duration * 1000) / 8
  // So: bitrate = (bytes * 8) / (duration * 1000)

  const bitrateKbps = Math.floor((targetSizeBytes * 8) / (estimatedDurationSeconds * 1000));

  // Ensure bitrate is reasonable (between 64kbps and 320kbps)
  return Math.max(64, Math.min(320, bitrateKbps));
}

// Get audio duration using ffprobe
function getAudioDuration(inputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg.ffprobe(inputPath, (err, metadata) => {
      if (err) {
        reject(err);
        return;
      }

      const duration = metadata.format.duration;
      resolve(duration);
    });
  });
}

// Convert M4A to compressed MP3 with visual progress
async function convertToMp3(inputPath, outputPath, customBitrate = null, showProgress = true) {
  return new Promise(async (resolve, reject) => {
    try {
      const filename = path.basename(inputPath);
      console.log(chalk.bold(`\n🎵 Converting: ${chalk.cyan(filename)}`));

      // Get audio duration
      const spinner = ora('Analyzing audio file...').start();
      const duration = await getAudioDuration(inputPath);
      spinner.succeed(`Duration: ${chalk.yellow(Math.round(duration) + 's')}`);

      // Calculate optimal bitrate
      const bitrate = customBitrate || calculateBitrate(duration);
      console.log(`🎯 Target bitrate: ${chalk.green(bitrate + 'kbps')}`);
      console.log(`📏 Target size: ${chalk.blue('Under 16MB')}`);

      // Ensure output directory exists
      await fs.ensureDir(path.dirname(outputPath));

      // Create progress bar
      let progressBar = null;
      if (showProgress) {
        progressBar = new cliProgress.SingleBar({
          format: chalk.cyan('{bar}') + ' {percentage}% | ETA: {eta}s | {value}/{total}',
          barCompleteChar: '\u2588',
          barIncompleteChar: '\u2591',
          hideCursor: true
        });
        progressBar.start(100, 0);
      }

      ffmpeg(inputPath)
        .toFormat('mp3')
        .audioBitrate(bitrate)
        .audioChannels(2) // Stereo
        .audioFrequency(44100) // Standard sample rate
        .on('progress', (progress) => {
          if (progressBar && progress.percent) {
            progressBar.update(Math.round(progress.percent));
          }
        })
        .on('end', async () => {
          if (progressBar) progressBar.stop();

          try {
            // Check output file size
            const stats = await stat(outputPath);
            const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);

            console.log(chalk.green(`\n✅ Conversion complete!`));
            console.log(`📁 Output: ${chalk.cyan(path.basename(outputPath))}`);
            console.log(`📏 Final size: ${chalk.blue(fileSizeMB + 'MB')}`);

            if (stats.size > MAX_FILE_SIZE_BYTES) {
              console.log(chalk.red(`⚠️  Warning: File exceeds ${MAX_FILE_SIZE_MB}MB limit.`));
              console.log(chalk.yellow(`💡 Consider using a lower bitrate or shorter audio.`));
            } else {
              console.log(chalk.green(`✅ File is under ${MAX_FILE_SIZE_MB}MB limit!`));
            }

            resolve({
              input: inputPath,
              output: outputPath,
              size: stats.size,
              bitrate: bitrate,
              duration: duration,
              compression: stats.size > MAX_FILE_SIZE_BYTES ? 'OVER_LIMIT' : 'OK'
            });
          } catch (error) {
            reject(error);
          }
        })
        .on('error', (err) => {
          if (progressBar) progressBar.stop();
          console.error(chalk.red(`\n❌ Error converting ${filename}:`), err.message);
          reject(err);
        })
        .save(outputPath);

    } catch (error) {
      reject(error);
    }
  });
}

// Find all M4A files in directory
async function findM4aFiles(directory) {
  try {
    const files = await readdir(directory);
    return files
      .filter(file => path.extname(file).toLowerCase() === '.m4a')
      .map(file => path.join(directory, file));
  } catch (error) {
    console.log(chalk.red(`Error reading directory ${directory}:`), error.message);
    return [];
  }
}

// Enhanced conversion function with visual feedback
async function convertAllM4aFiles(inputDir = './input', outputDir = './output', showProgress = true) {
  try {
    const spinner = ora('🔍 Scanning for M4A files...').start();
    const m4aFiles = await findM4aFiles(inputDir);
    spinner.stop();

    if (m4aFiles.length === 0) {
      console.log(chalk.yellow(`📁 No M4A files found in ${inputDir}`));
      return { success: 0, failed: 0, total: 0 };
    }

    console.log(chalk.bold(`\n🎵 Found ${chalk.cyan(m4aFiles.length)} M4A file(s):\n`));
    m4aFiles.forEach((file, index) => {
      console.log(`${chalk.yellow((index + 1).toString().padStart(2, ' '))}. ${chalk.white(path.basename(file))}`);
    });

    // Create output directory
    await fs.ensureDir(outputDir);

    const results = [];
    let successCount = 0;
    let failedCount = 0;

    console.log(chalk.bold(`\n🚀 Starting batch conversion...\n`));

    for (const m4aFile of m4aFiles) {
      const baseName = path.basename(m4aFile, '.m4a');
      const outputPath = path.join(outputDir, `${baseName}.mp3`);

      try {
        const result = await convertToMp3(m4aFile, outputPath, null, showProgress);
        results.push(result);
        successCount++;
      } catch (error) {
        console.error(chalk.red(`\n❌ Failed to convert ${path.basename(m4aFile)}:`), error.message);
        failedCount++;
      }
    }

    // Enhanced summary with visual table
    console.log(chalk.bold('\n' + '='.repeat(60)));
    console.log(chalk.bold('🎉 CONVERSION SUMMARY'));
    console.log(chalk.bold('='.repeat(60)));

    if (results.length > 0) {
      console.log(chalk.green(`✅ Successfully converted: ${successCount} file(s)`));

      results.forEach(result => {
        const sizeMB = (result.size / (1024 * 1024)).toFixed(2);
        const status = result.compression === 'OVER_LIMIT' ? chalk.red('⚠️  OVER LIMIT') : chalk.green('✅ OK');
        console.log(`  ${chalk.white(path.basename(result.output))}: ${chalk.blue(sizeMB + 'MB')} (${result.bitrate}kbps) ${status}`);
      });
    } else {
      console.log(chalk.yellow('📭 No files were successfully converted.'));
    }

    if (failedCount > 0) {
      console.log(chalk.red(`❌ Failed conversions: ${failedCount} file(s)`));
    }

    return { success: successCount, failed: failedCount, total: m4aFiles.length };

  } catch (error) {
    console.error(chalk.red('💥 Error:'), error.message);
    return { success: 0, failed: 1, total: 0 };
  }
}

// Handle command line arguments
async function main() {
  const args = process.argv.slice(2);

  // Show help
  if (args.includes('--help') || args.includes('-h')) {
    console.log(chalk.bold('\n🎵 M4A to MP3 Converter v2.0\n'));
    console.log('Usage:');
    console.log('  node convert.js [input-dir] [output-dir]');
    console.log('  node convert.js --single <input.m4a> [output.mp3]');
    console.log('  node convert.js --help');
    console.log('\nExamples:');
    console.log('  node convert.js                    # Convert from ./input to ./output');
    console.log('  node convert.js my-files out-files # Convert from my-files to out-files');
    console.log('  node convert.js --single file.m4a  # Convert single file');
    process.exit(0);
  }

  if (args.includes('--single')) {
    // Single file conversion mode
    const inputFile = args[args.indexOf('--single') + 1];
    const outputFile = args[args.indexOf('--single') + 2];

    if (!inputFile) {
      console.error(chalk.red('❌ Error: Please specify an input file'));
      console.log('Usage: node convert.js --single <input.m4a> [output.mp3]');
      process.exit(1);
    }

    const outputPath = outputFile || inputFile.replace('.m4a', '.mp3');

    try {
      await convertToMp3(inputFile, outputPath, null, true);
    } catch (error) {
      console.error(chalk.red('❌ Conversion failed:'), error.message);
      process.exit(1);
    }
  } else {
    // Batch conversion mode
    const inputDir = args[0] || './input';
    const outputDir = args[1] || './output';

    console.log(chalk.bold.blue('\n╔══════════════════════════════════════════════════════════════╗'));
    console.log(chalk.bold.blue('║                 🎵 M4A to MP3 Converter CLI                 ║'));
    console.log(chalk.bold.blue('╚══════════════════════════════════════════════════════════════╝\n'));

    const result = await convertAllM4aFiles(inputDir, outputDir, true);

    if (result.total > 0) {
      console.log(chalk.bold('\n📊 Final Results:'));
      console.log(`   Total files: ${chalk.cyan(result.total)}`);
      console.log(`   Successful: ${chalk.green(result.success)}`);
      if (result.failed > 0) {
        console.log(`   Failed: ${chalk.red(result.failed)}`);
      }
    }
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error(chalk.red('💥 Fatal error:'), error.message);
    process.exit(1);
  });
}

module.exports = {
  convertToMp3,
  convertAllM4aFiles,
  calculateBitrate
};
