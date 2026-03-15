#!/usr/bin/env node
/**
 * GitHub Repository Search Tool
 * 搜索 GitHub 仓库，支持多维度筛选
 */

import { githubFetch, formatDate, formatNumber, RateLimitError, NotFoundError, NetworkError } from './utils.mjs';

const GITHUB_API = 'https://api.github.com/search/repositories';

/**
 * Parse command-line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    query: '',
    language: null,
    minStars: 100,
    maxStars: null,
    updatedWithin: 365,
    createdAfter: null,
    sort: 'stars',
    order: 'desc',
    limit: 10,
    output: 'table'
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (!arg.startsWith('--')) {
      options.query = arg;
    } else if (arg === '--language' || arg === '-l') {
      options.language = args[++i];
    } else if (arg === '--min-stars') {
      options.minStars = parseInt(args[++i]);
    } else if (arg === '--max-stars') {
      options.maxStars = parseInt(args[++i]);
    } else if (arg === '--updated-within') {
      options.updatedWithin = parseInt(args[++i]);
    } else if (arg === '--created-after') {
      options.createdAfter = args[++i];
    } else if (arg === '--sort') {
      options.sort = args[++i];
    } else if (arg === '--order') {
      options.order = args[++i];
    } else if (arg === '--limit' || arg === '-n') {
      options.limit = parseInt(args[++i]);
    } else if (arg === '--output' || arg === '-o') {
      options.output = args[++i];
    }
  }

  return options;
}

/**
 * Build GitHub search query string
 */
function buildQuery(options) {
  let query = options.query;

  if (options.language) {
    query += ` language:${options.language}`;
  }

  if (options.minStars) {
    query += ` stars:>=${options.minStars}`;
  }

  if (options.maxStars) {
    query += ` stars:<=${options.maxStars}`;
  }

  if (options.updatedWithin) {
    const date = new Date();
    date.setDate(date.getDate() - options.updatedWithin);
    const dateStr = date.toISOString().split('T')[0];
    query += ` pushed:>=${dateStr}`;
  }

  if (options.createdAfter) {
    query += ` created:>=${options.createdAfter}`;
  }

  return query;
}

/**
 * Search GitHub repositories
 */
async function searchGitHub(query, sort, order, perPage = 30) {
  const url = `${GITHUB_API}?q=${encodeURIComponent(query)}&sort=${sort}&order=${order}&per_page=${perPage}`;
  return githubFetch(url);
}

/**
 * Generate Markdown table output
 */
function generateTable(repos, query) {
  let output = `## 🔥 GitHub 热门项目: ${query}\n\n`;
  output += '| 排名 | 项目 | ⭐ Stars | 🍴 Forks | 💻 语言 | 📅 更新 | 🔗 链接 |\n';
  output += '|-----|------|---------|---------|--------|--------|--------|\n';

  repos.forEach((repo, index) => {
    const name = repo.full_name;
    const stars = formatNumber(repo.stargazers_count);
    const forks = formatNumber(repo.forks_count);
    const lang = repo.language || 'N/A';
    const updated = formatDate(repo.pushed_at);
    const url = repo.html_url;

    output += `| ${index + 1} | ${name} | ${stars} | ${forks} | ${lang} | ${updated} | [查看](${url}) |\n`;
  });

  // Statistics summary
  const totalStars = repos.reduce((sum, r) => sum + r.stargazers_count, 0);
  const avgStars = Math.round(totalStars / repos.length);
  const languages = {};
  repos.forEach(r => {
    const lang = r.language || 'Unknown';
    languages[lang] = (languages[lang] || 0) + 1;
  });
  const mainLang = Object.entries(languages)
    .sort((a, b) => b[1] - a[1])
    .map(([lang, count]) => `${lang} (${Math.round(count / repos.length * 100)}%)`)
    .slice(0, 3)
    .join(', ');

  const recentlyUpdated = repos.filter(r => {
    const days = Math.floor((new Date() - new Date(r.pushed_at)) / (1000 * 60 * 60 * 24));
    return days <= 30;
  }).length;

  output += '\n### 📊 统计摘要\n';
  output += `- **总项目数**: ${repos.length}\n`;
  output += `- **平均 Stars**: ${formatNumber(avgStars)}\n`;
  output += `- **主要语言**: ${mainLang}\n`;
  output += `- **活跃度**: ${Math.round(recentlyUpdated / repos.length * 100)}% 最近30天有更新\n`;

  return output;
}

/**
 * Generate JSON output with rank field
 */
function generateJSON(repos, query) {
  return JSON.stringify({
    query,
    timestamp: new Date().toISOString(),
    total_count: repos.length,
    repositories: repos.map((repo, index) => ({
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
      license: repo.license?.name || 'N/A'
    }))
  }, null, 2);
}

/**
 * Generate CSV output
 */
function generateCSV(repos) {
  const headers = ['rank', 'full_name', 'description', 'stars', 'forks', 'language', 'updated_at', 'url'];
  let csv = headers.join(',') + '\n';

  repos.forEach((repo, index) => {
    const row = [
      index + 1,
      `"${repo.full_name}"`,
      `"${(repo.description || '').replace(/"/g, '""')}"`,
      repo.stargazers_count,
      repo.forks_count,
      repo.language || 'N/A',
      repo.pushed_at,
      repo.html_url
    ];
    csv += row.join(',') + '\n';
  });

  return csv;
}

/**
 * Main function
 */
async function main() {
  const options = parseArgs();

  if (!options.query) {
    console.log('用法: node github-search.mjs <关键词> [选项]');
    console.log('');
    console.log('选项:');
    console.log('  --language, -l     编程语言 (如: python, javascript)');
    console.log('  --min-stars        最小 stars 数 (默认: 100)');
    console.log('  --max-stars        最大 stars 数');
    console.log('  --updated-within   最近N天更新 (默认: 365)');
    console.log('  --created-after    创建日期之后 (如: 2024-01-01)');
    console.log('  --sort             排序方式: stars, updated, forks (默认: stars)');
    console.log('  --order            排序顺序: asc, desc (默认: desc)');
    console.log('  --limit, -n        返回结果数 (默认: 10)');
    console.log('  --output, -o       输出格式: table, json, csv (默认: table)');
    console.log('');
    console.log('示例:');
    console.log('  node github-search.mjs "agent memory"');
    console.log('  node github-search.mjs "rag" --language python --min-stars 1000');
    console.log('  node github-search.mjs "vector database" --limit 20 --output json');
    process.exit(1);
  }

  console.error(`🔍 搜索: "${options.query}"`);
  console.error(`📊 筛选: ${options.language ? '语言=' + options.language + ', ' : ''}stars>=${options.minStars}, 最近${options.updatedWithin}天更新`);
  console.error('⏳ 请求 GitHub API...\n');

  const query = buildQuery(options);
  console.error(`📝 查询语句: ${query}\n`);

  try {
    const data = await searchGitHub(query, options.sort, options.order, Math.min(options.limit, 100));

    if (!data || !data.items) {
      console.error('❌ 搜索失败或没有结果');
      process.exit(1);
    }

    const repos = data.items.slice(0, options.limit);

    console.error(`✅ 找到 ${data.total_count} 个项目，显示前 ${repos.length} 个\n`);

    // Generate output based on format
    let output;
    switch (options.output) {
      case 'json':
        output = generateJSON(repos, options.query);
        break;
      case 'csv':
        output = generateCSV(repos);
        break;
      case 'table':
      default:
        output = generateTable(repos, options.query);
        break;
    }

    console.log(output);
  } catch (error) {
    if (error instanceof RateLimitError) {
      console.error(`❌ 达到 API 频率限制`);
      console.error(`💡 提示: 设置 GITHUB_TOKEN 环境变量获取 5000 请求/小时的配额`);
      console.error(`   export GITHUB_TOKEN="ghp_your_token_here"`);
      process.exit(1);
    } else if (error instanceof NotFoundError) {
      console.error('❌ 资源不存在');
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
