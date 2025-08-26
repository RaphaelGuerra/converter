#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');

function checkFFmpeg() {
  const spinner = ora('🔍 Checking FFmpeg installation...').start();
  try {
    execSync('ffmpeg -version', { stdio: 'pipe' });
    spinner.succeed(chalk.green('✅ FFmpeg is installed'));
    return true;
  } catch (error) {
    spinner.fail(chalk.red('❌ FFmpeg is not installed'));
    return false;
  }
}

function installDependencies() {
  const spinner = ora('📦 Installing Node.js dependencies...').start();
  try {
    execSync('npm install', { stdio: 'pipe' });
    spinner.succeed(chalk.green('✅ Dependencies installed successfully'));
    return true;
  } catch (error) {
    spinner.fail(chalk.red('❌ Failed to install dependencies'));
    console.error(chalk.red('Error:'), error.message);
    return false;
  }
}

function createDirectories() {
  const spinner = ora('📁 Creating project directories...').start();
  const dirs = ['./input', './output', './test-files'];

  let created = 0;
  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      created++;
    }
  });

  if (created > 0) {
    spinner.succeed(chalk.green(`✅ Created ${created} directories`));
  } else {
    spinner.info(chalk.blue('📁 All directories already exist'));
  }

  // Show directory structure
  console.log(chalk.bold('\n📂 Project Structure:'));
  console.log(`  ${chalk.cyan('input/')}     → Place your .m4a files here`);
  console.log(`  ${chalk.cyan('output/')}    → Converted .mp3 files appear here`);
  console.log(`  ${chalk.cyan('test-files/')} → Test files directory`);
}

function showNextSteps() {
  console.log(chalk.bold('\n🎯 Next Steps:'));
  console.log(`  1. ${chalk.yellow('Place your .m4a files in the input/ directory')}`);
  console.log(`  2. ${chalk.yellow('Run: npm run convert')} (interactive menu)`);
  console.log(`  3. ${chalk.yellow('Or run: npm run convert-cli')} (command line)`);
  console.log(`  4. ${chalk.yellow('Find your MP3s in the output/ directory')}`);

  console.log(chalk.bold('\n📚 Available Commands:'));
  console.log(`  ${chalk.cyan('npm run convert')}       → Interactive menu with visual progress`);
  console.log(`  ${chalk.cyan('npm run convert-cli')}   → Command line interface`);
  console.log(`  ${chalk.cyan('npm run setup')}         → Run setup again`);
  console.log(`  ${chalk.cyan('npm run convert-single')} → Convert single file`);
}

function showWelcome() {
  console.clear();
  console.log(chalk.bold.blue(`
╔══════════════════════════════════════════════════════════════╗
║                 🎵 M4A to MP3 Converter v2.0                 ║
║                      Setup & Installation                    ║
╚══════════════════════════════════════════════════════════════╝
`));
}

async function main() {
  showWelcome();

  console.log(chalk.bold('🚀 Setting up M4A to MP3 Converter with Interactive CLI...\n'));

  let allGood = true;

  // Check FFmpeg
  const ffmpegInstalled = checkFFmpeg();
  if (!ffmpegInstalled) {
    console.log(chalk.bold('\n🔧 FFmpeg Installation Guide:'));
    console.log(`  ${chalk.cyan('macOS:')} brew install ffmpeg`);
    console.log(`  ${chalk.cyan('Ubuntu/Debian:')} sudo apt install ffmpeg`);
    console.log(`  ${chalk.cyan('Windows:')} Download from https://ffmpeg.org/download.html`);
    console.log(chalk.yellow('\nAfter installing FFmpeg, run this setup script again.\n'));
    allGood = false;
  }

  // Install dependencies
  if (ffmpegInstalled) {
    const depsInstalled = installDependencies();
    if (!depsInstalled) {
      allGood = false;
    }
  }

  // Create directories
  if (allGood) {
    createDirectories();
  }

  // Final status
  if (allGood) {
    console.log(chalk.bold.green('\n🎉 Setup Complete!'));
    showNextSteps();
  } else {
    console.log(chalk.bold.red('\n❌ Setup Incomplete'));
    console.log(chalk.yellow('Please resolve the issues above and run setup again.'));
  }

  console.log(chalk.bold('\n' + '='.repeat(60)));
}

if (require.main === module) {
  main().catch(error => {
    console.error(chalk.red('💥 Setup error:'), error.message);
    process.exit(1);
  });
}
