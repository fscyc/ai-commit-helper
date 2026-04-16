#!/usr/bin/env node

/**
 * Node.js CLI wrapper for AI Commit Helper
 * This is a wrapper that calls the Python version if available,
 * or provides a fallback implementation.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Check if Python version is available
function hasPythonVersion() {
  const pythonPackagePath = path.join(__dirname, '..', 'src', 'ai_commit_helper');
  const setupPyPath = path.join(__dirname, '..', 'setup.py');
  
  return fs.existsSync(pythonPackagePath) || fs.existsSync(setupPyPath);
}

// Call Python version
function callPythonVersion(args) {
  return new Promise((resolve, reject) => {
    // Try to find Python executable
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    
    // Check if installed via pip
    const scriptPath = path.join(__dirname, '..', 'src', 'ai_commit_helper', 'cli.py');
    const moduleSpec = fs.existsSync(scriptPath) 
      ? scriptPath 
      : '-m ai_commit_helper.cli';
    
    const child = spawn(pythonCmd, [moduleSpec, ...args], {
      stdio: 'inherit',
      shell: true
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Python process exited with code ${code}`));
      }
    });
    
    child.on('error', (err) => {
      reject(err);
    });
  });
}

// Fallback Node.js implementation
function nodeImplementation(args) {
  console.log('AI Commit Helper - Node.js Fallback');
  console.log('====================================');
  console.log('This is a placeholder implementation.');
  console.log('Please install the Python version for full functionality:');
  console.log('');
  console.log('  pip install ai-commit-helper');
  console.log('');
  console.log('Or use the Python version directly:');
  console.log('  python -m ai_commit_helper.cli');
  console.log('');
  console.log('Arguments received:', args);
  
  // Show help
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log('');
    console.log('Usage: aicommit [options]');
    console.log('');
    console.log('Options:');
    console.log('  --help, -h     Show this help message');
    console.log('  --version      Show version');
    console.log('  --format <fmt> Output format (conventional, zh, emoji)');
    console.log('  --batch <n>    Generate multiple options');
    console.log('  --no-staged    Use unstaged changes instead of staged');
    console.log('  --no-color     Disable colored output');
    console.log('  generate       Generate commit message');
    console.log('  interactive    Interactive mode');
    console.log('  serve          Start web server');
    console.log('');
  }
  
  if (args.includes('--version')) {
    console.log('ai-commit-helper v0.1.0 (Node.js wrapper)');
  }
  
  return Promise.resolve();
}

// Main function
async function main() {
  const args = process.argv.slice(2);
  
  try {
    if (hasPythonVersion()) {
      await callPythonVersion(args);
    } else {
      await nodeImplementation(args);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main, hasPythonVersion, callPythonVersion };