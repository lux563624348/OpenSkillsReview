#!/usr/bin/env node
/**
 * GitHub Repository Detail Fetcher
 * 获取单个仓库的详细信息
 */

import { githubFetch, formatDate, formatNumber, RateLimitError, NotFoundError, NetworkError } from './utils.mjs';

const GITHUB_API = 'https://api.github.com/repos';

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    return null;
  }
  return args[0]; // repo full name, e.g., "microsoft/autogen"
}

/**
 * Fetch repository details from GitHub API
 */
async function fetchRepoDetails(repoFullName) {
  const url = `${GITHUB_API}/${repoFullName}`;
  return githubFetch(url);
}

/**
 * Fetch contributors for the repository
 */
async function fetchContributors(repoFullName) {
  const url = `${GITHUB_API}/${repoFullName}/contributors?per_page=10`;
  try {
    return await githubFetch(url);
  } catch (error) {
    // Contributors endpoint may fail gracefully
    return [];
  }
}

/**
 * Calculate activity level based on last push
 */
function getActivityLevel(pushedAt) {
  const days = Math.floor((new Date() - new Date(pushedAt)) / (1000 * 60 * 60 * 24));
  if (days <= 7) return '🟢 非常活跃';
  if (days <= 30) return '🟡 活跃';
  if (days <= 90) return '🟠 一般';
  return '🔴 不活跃';
}

/**
 * Generate Markdown report for repository
 */
function generateReport(repo, contributors) {
  let output = `## 📋 项目详情: ${repo.full_name}\n\n`;

  // Basic info
  output += `**名称**: ${repo.name}\n`;
  output += `**描述**: ${repo.description || '无描述'}\n`;
  output += `**🏷️ 标签**: ${repo.topics?.join(', ') || '无标签'}\n\n`;

  // Statistics
  output += `### 📈 数据统计\n`;
  output += `- ⭐ **Stars**: ${formatNumber(repo.stargazers_count)}\n`;
  output += `- 🍴 **Forks**: ${formatNumber(repo.forks_count)}\n`;
  output += `- 👁️ **Watchers**: ${formatNumber(repo.watchers_count)}\n`;
  output += `- 🐛 **Open Issues**: ${repo.open_issues_count}\n\n`;

  // Code info
  output += `### 💻 代码信息\n`;
  output += `- **主要语言**: ${repo.language || 'N/A'}\n`;
  output += `- **许可证**: ${repo.license?.name || 'N/A'}\n`;
  output += `- **默认分支**: ${repo.default_branch}\n`;
  output += `- **仓库大小**: ${formatNumber(repo.size)} kB\n\n`;

  // Activity
  output += `### 📅 活跃度\n`;
  output += `- **最后提交**: ${formatDate(repo.pushed_at)} (${getActivityLevel(repo.pushed_at)})\n`;
  output += `- **创建时间**: ${formatDate(repo.created_at)}\n`;
  output += `- **更新时间**: ${formatDate(repo.updated_at)}\n`;

  if (contributors && contributors.length > 0) {
    output += `- **主要贡献者**: ${contributors.slice(0, 5).map(c => c.login).join(', ')}\n`;
  }
  output += '\n';

  // Links
  output += `### 🔗 链接\n`;
  output += `- **仓库**: ${repo.html_url}\n`;
  if (repo.homepage) {
    output += `- **主页**: ${repo.homepage}\n`;
  }
  output += `- **Issues**: ${repo.html_url}/issues\n`;
  output += `- **Pull Requests**: ${repo.html_url}/pulls\n`;

  return output;
}

/**
 * Main function
 */
async function main() {
  const repoFullName = parseArgs();

  if (!repoFullName) {
    console.log('用法: node repo-detail.mjs <owner/repo>');
    console.log('');
    console.log('示例:');
    console.log('  node repo-detail.mjs microsoft/autogen');
    console.log('  node repo-detail.mjs langchain-ai/langchain');
    process.exit(1);
  }

  console.error(`🔍 获取仓库详情: ${repoFullName}\n`);

  const [owner, repo] = repoFullName.split('/');
  if (!owner || !repo) {
    console.error('❌ 格式错误，请使用 "owner/repo" 格式');
    process.exit(1);
  }

  try {
    const repoData = await fetchRepoDetails(repoFullName);

    console.error('📊 获取贡献者信息...');
    const contributors = await fetchContributors(repoFullName);

    console.error('✅ 完成\n');

    const report = generateReport(repoData, contributors);
    console.log(report);
  } catch (error) {
    if (error instanceof NotFoundError) {
      console.error(`❌ 仓库不存在: ${repoFullName}`);
      process.exit(1);
    } else if (error instanceof RateLimitError) {
      console.error(`❌ 达到 API 频率限制`);
      console.error(`💡 提示: 设置 GITHUB_TOKEN 环境变量获取 5000 请求/小时的配额`);
      console.error(`   export GITHUB_TOKEN="ghp_your_token_here"`);
      process.exit(1);
    } else if (error instanceof NetworkError) {
      console.error(`❌ ${error.message}`);
      process.exit(1);
    } else {
      console.error(`❌ 错误: ${error.message}`);
      process.exit(1);
    }
  }
}

main();
