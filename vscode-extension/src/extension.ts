import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  console.log('AI Commit Helper extension is now active!');

  // Check if Python version is available
  const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  const config = vscode.workspace.getConfiguration('aiCommitHelper');
  
  // Command: Generate commit message
  const generateCommand = vscode.commands.registerCommand('ai-commit-helper.generate', async () => {
    const format = config.get('format', 'conventional');
    await runAicommit(['--format', format]);
  });

  // Command: Generate from staged changes
  const generateFromChangesCommand = vscode.commands.registerCommand('ai-commit-helper.generateFromChanges', async () => {
    const format = config.get('format', 'conventional');
    await runAicommit(['--format', format]);
  });

  // Command: Generate from unstaged changes
  const generateFromUnstagedCommand = vscode.commands.registerCommand('ai-commit-helper.generateFromUnstaged', async () => {
    const format = config.get('format', 'conventional');
    await runAicommit(['--format', format, '--no-staged']);
  });

  // Command: Open Web UI
  const openWebUICommand = vscode.commands.registerCommand('ai-commit-helper.openWebUI', async () => {
    // Start web server if not running
    const port = 8000;
    const child = cp.spawn('aicommit', ['serve', '--port', port.toString()], {
      detached: true,
      stdio: 'ignore'
    });
    child.unref();

    // Open browser
    vscode.env.openExternal(vscode.Uri.parse(`http://localhost:${port}`));
    
    vscode.window.showInformationMessage(`Web UI started at http://localhost:${port}`);
  });

  context.subscriptions.push(
    generateCommand,
    generateFromChangesCommand,
    generateFromUnstagedCommand,
    openWebUICommand
  );
}

export function deactivate() {
  // Cleanup if needed
}

async function runAicommit(args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const terminal = vscode.window.createTerminal('AI Commit Helper');
    terminal.show();
    
    // Build command
    const command = `aicommit ${args.join(' ')}`;
    terminal.sendText(command);
    
    vscode.window.showInformationMessage(`Running: ${command}`);
    resolve();
  });
}

// Check if aicommit is available
function checkAicommitAvailable(): Promise<boolean> {
  return new Promise((resolve) => {
    cp.exec('aicommit --version', (error) => {
      if (error) {
        cp.exec('python -m ai_commit_helper.cli --version', (error2) => {
          resolve(!error2);
        });
      } else {
        resolve(true);
      }
    });
  });
}