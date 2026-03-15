#!/usr/bin/env node
/**
 * Batch Repository Detail Fetcher
 * 批量获取多个仓库的详细信息
 * 可以从标准输入 (JSON 数组或搜索结果) 或命令行参数读取仓库列表
 */

import { githubFetch, formatDate, formatNumber, RateLimitError, NotFoundError, NetworkError } from './utils.mjs';
import readline from 'readline';

const GITHUB_API = 'https://api.github.com/repos';

/**
 * Fetch repository details
 */
async function fetchRepoDetails(repoFullName) {
  const url = `${GITHUB_API}/${repoFullName}`;
  return githubFetch(url);
}

/**
 * Fetch contributors
 */
async function fetchContributors(repoFullName) {
  const url = `${GITHUB_API}/${repoFullName}/contributors?per_page=10`;
  try {
    return await githubFetch(url);
  } catch (error) {
    return [];
  }
}

/**
 * Calculate activity level
 */
function getActivityLevel(pushedAt) {
  const days = Math.floor((new Date() - new Date(pushedAt)) / (1000 * 60 * 60 * 24));
  if (days <= 7) return '🟢 非常活跃';
  if (days <= 30) return '🟡 活跃';
  if (days <= 90) return '🟠 一般';
  return '🔴 不活跃';
}

/**
 * Generate Markdown section for a repository
 */
function generateRepoSection(repo, index) {
  let output = `### ${index}. ${repo.full_name}\n\n`;

  output += `**描述**: ${repo.description || '无描述'}\n`;
  output += `**🏷️ 标签**: ${repo.topics?.join(', ') || '无标签'}\n\n`;

  output += `**📈 统计**: `;
  output += `⭐ ${formatNumber(repo.stargazers_count)} | `;
  output += `🍴 ${formatNumber(repo.forks_count)} | `;
  output += `👁️ ${formatNumber(repo.watchers_count)}\n`;

  output += `**💻 代码**: `;
  output += `${repo.language || 'N/A'} | `;
  output += `${formatNumber(repo.size)} kB | `;
  output += `${repo.license?.name || 'N/A'}\n`;

  output += `**📅 活动**: ${getActivityLevel(repo.pushed_at)} | `;
  output += `最后提交 ${formatDate(repo.pushed_at)}\n`;

  output += `**🔗 链接**: [仓库](${repo.html_url}) | `;
  output += `[Issues](${repo.html_url}/issues) | `;
  output += `[PRs](${repo.html_url}/pulls)\n\n`;

  return output;
}

/**
 * Generate JSON output for batch
 */
function generateJSON(results) {
  return JSON.stringify({
    timestamp: new Date().toISOString(),
    total_count: results.length,
    repositories: results.map((repo, index) => ({
      rank: index + 1,
      full_name: repo.full_name,
      description: repo.description,
      html_url: repo.html_url,
      stargazers_count: repo.stargazers_count,
      forks_count: repo.forks_count,
      language: repo.language,
      pushed_at: repo.pushed_at,
      created_at: repo.created_at,
      topics: repo.topics || [],
      license: repo.license?.name || 'N/A',
      size_kb: repo.size
    }))
  }, null, 2);
}

/**
 * Generate Markdown report for batch
 */
function generateMarkdown(results) {
  let output = `# 📋 批量仓库详情报告\n\n`;
  output += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n`;
  output += `**总仓库数**: ${results.length}\n\n`;

  // Summary stats
  const totalStars = results.reduce((sum, r) => sum + r.stargazers_count, 0);
  const avgStars = Math.round(totalStars / results.length);
  const languages = {};
  results.forEach(r => {
    const lang = r.language || 'Unknown';
    languages[lang] = (languages[lang] || 0) + 1;
  });
  const mainLangs = Object.entries(languages)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([lang, count]) => `${lang} (${count})`)
    .join(', ');

  output += `## 📊 统计汇总\n\n`;
  output += `- **总 Stars**: ${formatNumber(totalStars)}\n`;
  output += `- **平均 Stars**: ${formatNumber(avgStars)}\n`;
  output += `- **主要语言**: ${mainLangs}\n\n`;

  output += `## 📚 详细列表\n\n`;

  results.forEach((repo, index) => {
    output += generateRepoSection(repo, index + 1);
  });

  return output;
}

/**
 * Read repository list from stdin (JSON format)
 */
async function readFromStdin() {
  return new Promise((resolve, reject) => {
    let data = '';

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false
    });

    rl.on('line', (line) => {
      data += line;
    });

    rl.on('close', () => {
      try {
        if (!data.trim()) {
          resolve([]);
          return;
        }

        const parsed = JSON.parse(data);

        // Handle different JSON formats
        let repos = [];
        if (Array.isArray(parsed)) {
          if (parsed.length > 0 && typeof parsed[0] === 'string') {
            // Array of repo names: ["owner/repo", ...]
            repos = parsed;
          } else if (parsed.length > 0 && parsed[0].full_name) {
            // Array of repo objects with full_name field
            repos = parsed.map(r => r.full_name);
          } else if (parsed.length > 0 && parsed[0].repositories) {
            // Search results format with repositories array
            repos = parsed[0].repositories.map(r => r.full_name);
          }
        } else if (parsed.repositories && Array.isArray(parsed.repositories)) {
          // Search result object with repositories array
          repos = parsed.repositories.map(r => r.full_name);
        }

        resolve(repos);
      } catch (error) {
        reject(new Error(`Invalid JSON input: ${error.message}`));
      }
    });

    rl.on('error', reject);
  });
}

/**
 * Show help message
 */
function showHelp() {
  console.log('用法: node batch-detail.mjs [仓库列表]\n');
  console.log('从标准输入读取:');
  console.log('  cat search-results.json | node batch-detail.mjs');
  console.log('  node github-search.mjs "agent" --output json | node batch-detail.mjs\n');
  console.log('从命令行参数读取:');
  console.log('  node batch-detail.mjs "microsoft/autogen" "langchain-ai/langchain"\n');
  console.log('输入格式支持:');
  console.log('  - JSON 数组: ["owner/repo", "owner/repo"]');
  console.log('  - JSON 对象数组: [{full_name: "owner/repo"}, ...]');
  console.log('  - 搜索结果 JSON: {repositories: [{full_name: "owner/repo"}, ...]}');
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2);
  let repoNames = [];

  // Check for help flag
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }

  // Check if input is from stdin or command-line args
  if (!process.stdin.isTTY) {
    // Input from pipe
    try {
      repoNames = await readFromStdin();
    } catch (error) {
      console.error(`❌ 标准输入错误: ${error.message}`);
      process.exit(1);
    }
  } else if (args.length > 0) {
    // Command-line arguments
    repoNames = args;
  }

  if (repoNames.length === 0 && process.stdin.isTTY) {
    // Show help if running interactively with no args
    showHelp();
    process.exit(0);
  }

  if (repoNames.length === 0) {
    console.error('❌ 没有提供仓库列表');
    process.exit(1);
  }

  console.error(`🔍 批量获取 ${repoNames.length} 个仓库的详细信息...\n`);

  const results = [];
  const errors = [];

  for (let i = 0; i < repoNames.length; i++) {
    const repoName = repoNames[i].trim();

    if (!repoName) continue;

    try {
      console.error(`⏳ [${i + 1}/${repoNames.length}] ${repoName}`);

      const repoData = await fetchRepoDetails(repoName);
      results.push(repoData);

      console.error(`  ✅ 成功`);

      // Add small delay to avoid hitting rate limits
      if (i < repoNames.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    } catch (error) {
      if (error instanceof NotFoundError) {
        console.error(`  ❌ 不存在`);
        errors.push({ repo: repoName, error: 'Not found' });
      } else if (error instanceof RateLimitError) {
        console.error(`  ❌ 频率限制`);
        errors.push({ repo: repoName, error: 'Rate limit' });
        break;
      } else {
        console.error(`  ❌ ${error.message}`);
        errors.push({ repo: repoName, error: error.message });
      }
    }
  }

  console.error(`\n✅ 完成: 成功获取 ${results.length}/${repoNames.length} 个仓库\n`);

  if (errors.length > 0) {
    console.error(`⚠️ 失败列表:`);
    errors.forEach(({ repo, error }) => {
      console.error(`  - ${repo}: ${error}`);
    });
    console.error('');
  }

  if (results.length === 0) {
    console.error('❌ 没有成功获取任何仓库');
    process.exit(1);
  }

  // Output results
  const output = generateMarkdown(results);
  console.log(output);
}

main().catch(err => {
  console.error(`❌ 错误: ${err.message}`);
  process.exit(1);
});
