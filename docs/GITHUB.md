# GitHub Setup Guide

A guide to setting up your GitHub account and repository access for contributing to the Nice Connectives project.

---

## Table of Contents

- [Creating a GitHub Account](#creating-a-github-account)
- [Fork vs Clone: Which Do You Need?](#fork-vs-clone-which-do-you-need)
- [Forking the Repository](#forking-the-repository)
- [Setting Up SSH Keys](#setting-up-ssh-keys)
- [Uploading Your SSH Key to GitHub](#uploading-your-ssh-key-to-github)
- [Verifying Your SSH Connection](#verifying-your-ssh-connection)
- [Converting a Clone to a Fork](#converting-a-clone-to-a-fork)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Creating a GitHub Account

If you don't already have a GitHub account:

1. Visit [github.com](https://github.com)
2. Click "Sign up" in the top right
3. Follow the prompts to create your account:
   - Enter your email address
   - Create a password
   - Choose a username
   - Verify your account (email verification)

**Note**: Your GitHub username will be visible in contributions, so choose something professional or memorable.

---

## Fork vs Clone: Which Do You Need?

### Quick Decision Guide

**Use Fork if:**
- You want to contribute changes back to the project
- You plan to submit pull requests
- You need your own copy to experiment with

**Use Clone if:**
- You only want to run the code locally
- You don't plan to contribute changes
- You just want to explore the codebase

### What's the Difference?

**Fork**:
- Creates your own copy of the repository on GitHub
- You can make changes and propose them back to the original
- Required for contributing via pull requests
- Example URL: `https://github.com/YOUR-USERNAME/nice_connectives`

**Clone**:
- Downloads the repository to your local machine
- You can run and modify code locally
- Changes stay on your machine unless you have write access
- Example: `git clone https://github.com/benbrastmckie/Connectives.git`

### Don't Worry!

If you cloned but realize you need to fork, you can easily [convert your clone to use your fork](#converting-a-clone-to-a-fork) later.

---

## Forking the Repository

To create your own copy of the repository on GitHub:

### Step 1: Navigate to the Repository

Visit the repository page:
```
https://github.com/benbrastmckie/Connectives
```

### Step 2: Click the Fork Button

1. Look for the "Fork" button in the top right corner of the page
2. Click "Fork"
3. GitHub will create a copy under your account
4. You'll be redirected to your fork: `https://github.com/YOUR-USERNAME/nice_connectives`

### Step 3: Clone Your Fork

Now clone your fork to your local machine:

**Using HTTPS (easier, no SSH setup needed):**
```bash
git clone https://github.com/YOUR-USERNAME/nice_connectives.git
cd nice_connectives
```

**Using SSH (recommended for regular contributors):**
```bash
git clone git@github.com:YOUR-USERNAME/nice_connectives.git
cd nice_connectives
```

**Note**: Replace `YOUR-USERNAME` with your actual GitHub username.

For SSH, you'll need to [set up SSH keys](#setting-up-ssh-keys) first (see next section).

---

## Setting Up SSH Keys

SSH keys allow you to connect to GitHub without entering your password every time. This is the recommended approach for regular contributors.

### Why Use SSH Keys?

- **Security**: More secure than password authentication
- **Convenience**: No need to enter credentials for every push/pull
- **Required**: Many operations require SSH authentication

### Check for Existing Keys

Before creating new keys, check if you already have SSH keys:

**Linux/macOS:**
```bash
ls -la ~/.ssh
```

**Windows (PowerShell):**
```powershell
dir $env:USERPROFILE\.ssh
```

Look for files named:
- `id_rsa.pub` (RSA key - older)
- `id_ed25519.pub` (ED25519 key - recommended)

If you see these files, you already have SSH keys! Skip to [Uploading Your SSH Key](#uploading-your-ssh-key-to-github).

### Generate New SSH Keys

If you don't have SSH keys, create them:

#### Linux/macOS

```bash
# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Or if your system doesn't support ED25519, use RSA:
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

**Follow the prompts:**
1. **File location**: Press Enter to accept default (`~/.ssh/id_ed25519`)
2. **Passphrase**: Enter a passphrase (recommended) or press Enter for none
3. **Confirm passphrase**: Re-enter your passphrase

#### Windows

**Option 1: Using PowerShell**
```powershell
# Generate ED25519 key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Or RSA if ED25519 not supported:
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

**Option 2: Using Git Bash** (if installed with Git for Windows)
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

**Follow the prompts** (same as Linux/macOS above).

### Start the SSH Agent

After generating keys, start the SSH agent:

**Linux/macOS:**
```bash
# Start the agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519
# Or for RSA: ssh-add ~/.ssh/id_rsa
```

**Windows (PowerShell):**
```powershell
# Start the agent
Start-Service ssh-agent

# Add your key
ssh-add $env:USERPROFILE\.ssh\id_ed25519
# Or for RSA: ssh-add $env:USERPROFILE\.ssh\id_rsa
```

---

## Uploading Your SSH Key to GitHub

Now you need to add your public key to your GitHub account.

### Step 1: Copy Your Public Key

**Linux:**
```bash
# Copy to clipboard (requires xclip)
sudo apt install xclip  # If not installed
xclip -selection clipboard < ~/.ssh/id_ed25519.pub

# Or display to copy manually:
cat ~/.ssh/id_ed25519.pub
```

**macOS:**
```bash
# Copy to clipboard
pbcopy < ~/.ssh/id_ed25519.pub

# Or display to copy manually:
cat ~/.ssh/id_ed25519.pub
```

**Windows (PowerShell):**
```powershell
# Copy to clipboard
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# Or display to copy manually:
type $env:USERPROFILE\.ssh\id_ed25519.pub
```

**Note**: Use `id_rsa.pub` instead of `id_ed25519.pub` if you generated an RSA key.

### Step 2: Add Key to GitHub

1. Visit [github.com](https://github.com) and log in
2. Click your profile picture (top right) → **Settings**
3. In the left sidebar, click **SSH and GPG keys**
4. Click **New SSH key** (green button)
5. Fill in the form:
   - **Title**: A descriptive name (e.g., "Personal Laptop" or "Work Desktop")
   - **Key type**: Select "Authentication Key"
   - **Key**: Paste your public key (copied in Step 1)
6. Click **Add SSH key**
7. Confirm with your GitHub password if prompted

---

## Verifying Your SSH Connection

Test that your SSH connection to GitHub works:

```bash
ssh -T git@github.com
```

**Expected output:**
```
Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see this message, your SSH setup is working correctly!

**First time connecting?**

You may see a message about the authenticity of the host:
```
The authenticity of host 'github.com' can't be established.
ED25519 key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter. This is normal for the first connection.

---

## Converting a Clone to a Fork

If you cloned the original repository but now want to contribute, you can redirect your clone to use your fork instead.

### Step 1: Fork the Repository on GitHub

Follow the [Forking the Repository](#forking-the-repository) section above to create your fork.

### Step 2: Update Remote URL

Update your local repository to point to your fork:

```bash
# Check current remote
git remote -v
# Should show: origin  https://github.com/benbrastmckie/Connectives.git (fetch)

# Update to your fork (HTTPS)
git remote set-url origin https://github.com/YOUR-USERNAME/nice_connectives.git

# Or update to your fork (SSH)
git remote set-url origin git@github.com:YOUR-USERNAME/nice_connectives.git

# Verify the change
git remote -v
# Should now show your fork URL
```

### Step 3: Add Upstream Remote

Add the original repository as "upstream" to pull future updates:

```bash
# Add upstream remote
git remote add upstream https://github.com/benbrastmckie/Connectives.git

# Verify remotes
git remote -v
# Should show both origin (your fork) and upstream (original)
```

Now you can:
- Push to your fork: `git push origin branch-name`
- Pull updates from original: `git pull upstream master`

---

## Troubleshooting

### "Permission denied (publickey)"

**Problem**: SSH connection fails with permission denied error.

**Solutions**:

1. **Check SSH agent is running:**
   ```bash
   # Linux/macOS
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

   # Windows
   Start-Service ssh-agent
   ssh-add $env:USERPROFILE\.ssh\id_ed25519
   ```

2. **Verify key is added to GitHub:**
   - Go to GitHub Settings → SSH and GPG keys
   - Ensure your public key is listed
   - Try removing and re-adding the key

3. **Check key file permissions (Linux/macOS):**
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```

4. **Use HTTPS instead:**
   If SSH continues to fail, use HTTPS URLs temporarily:
   ```bash
   git remote set-url origin https://github.com/YOUR-USERNAME/nice_connectives.git
   ```

### "Could not open a connection to your authentication agent"

**Problem**: SSH agent not running.

**Solution**:
```bash
# Linux/macOS
eval "$(ssh-agent -s)"

# Windows PowerShell (as Administrator)
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

### "Host key verification failed"

**Problem**: GitHub's host key not in known_hosts file.

**Solution**:
```bash
# Remove old key (if exists)
ssh-keygen -R github.com

# Connect and accept new key
ssh -T git@github.com
# Type 'yes' when prompted
```

### "git@github.com: Permission denied (publickey)" on Windows

**Problem**: Windows SSH agent not configured correctly.

**Solutions**:

1. **Use Git Bash instead of PowerShell:**
   - Git Bash has better SSH support
   - Installed with Git for Windows

2. **Configure Windows SSH agent:**
   ```powershell
   # Run PowerShell as Administrator
   Get-Service ssh-agent | Set-Service -StartupType Automatic
   Start-Service ssh-agent
   ```

3. **Use HTTPS authentication:**
   - Switch to HTTPS URLs (easier on Windows)
   - Use GitHub Personal Access Token for authentication

### Cannot Find `.ssh` Directory

**Problem**: `~/.ssh` directory doesn't exist.

**Solution**:
```bash
# Linux/macOS
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Windows PowerShell
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.ssh
```

Then generate SSH keys following the [Setting Up SSH Keys](#setting-up-ssh-keys) section.

### Fork Button Not Visible

**Problem**: Can't find Fork button on repository page.

**Solution**:
- Make sure you're logged into GitHub
- You might already have a fork (check your repositories)
- If repository is private, you may not have permission to fork

---

## Next Steps

Now that you have GitHub set up:

1. **Complete Installation**: Follow [INSTALLATION.md](INSTALLATION.md) to set up your development environment
2. **Learn the Contribution Workflow**: Read [CONTRIBUTING.md](CONTRIBUTING.md) for how to create branches, make changes, and submit pull requests
3. **Get AI Assistance**: Use [Claude Code](CLAUDE_CODE.md) for interactive help with Git, GitHub, and development

### Quick Links

- **[Installation Guide](INSTALLATION.md)** - Set up Python, dependencies, and verify installation
- **[Contributing Guide](CONTRIBUTING.md)** - Complete contribution workflow
- **[Usage Guide](USAGE.md)** - Learn how to use the CLI and run searches
- **[Claude Code Guide](CLAUDE_CODE.md)** - Get AI assistance with development
- **[Main README](../README.md)** - Project overview and documentation

---

**Ready to contribute? Continue to the [Contributing Guide](CONTRIBUTING.md)!**
