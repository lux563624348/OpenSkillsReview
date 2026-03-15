/**
 * Shared utilities for GitHub Research skill
 */

/**
 * Build headers object for GitHub API requests
 * @param {string} [token] - Optional GitHub API token
 * @returns {Object} Headers object
 */
export function getHeaders(token = null) {
  const headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'GitHub-Research-Skill'
  };

  if (token || process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `token ${token || process.env.GITHUB_TOKEN}`;
  }

  return headers;
}

/**
 * Custom error classes for different API failure modes
 */
export class RateLimitError extends Error {
  constructor(remaining = 0, resetTime = null) {
    super(`Rate limit exceeded (${remaining} requests remaining)`);
    this.name = 'RateLimitError';
    this.remaining = remaining;
    this.resetTime = resetTime;
  }
}

export class NotFoundError extends Error {
  constructor(resource = 'Resource') {
    super(`${resource} not found (404)`);
    this.name = 'NotFoundError';
  }
}

export class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
  }
}

/**
 * Fetch and parse JSON from GitHub API with error handling
 * @param {string} url - API endpoint URL
 * @param {string} [token] - Optional GitHub API token
 * @returns {Promise<Object>} Parsed JSON response
 * @throws {RateLimitError} When rate limit is hit
 * @throws {NotFoundError} When resource not found
 * @throws {NetworkError} On network/connection errors
 */
export async function githubFetch(url, token = null) {
  try {
    const response = await fetch(url, {
      headers: getHeaders(token),
      timeout: 30000
    });

    // Check for rate limit
    const remaining = response.headers.get('x-ratelimit-remaining');
    const resetTime = response.headers.get('x-ratelimit-reset');

    if (response.status === 403 && remaining === '0') {
      throw new RateLimitError(0, resetTime);
    }

    // Check for not found
    if (response.status === 404) {
      throw new NotFoundError();
    }

    // Check for other HTTP errors
    if (!response.ok) {
      throw new NetworkError(`GitHub API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof RateLimitError || error instanceof NotFoundError || error instanceof NetworkError) {
      throw error;
    }
    throw new NetworkError(`Cannot reach GitHub API: ${error.message}`);
  }
}

/**
 * Format date as relative string in Chinese
 * @param {string} dateStr - ISO date string
 * @returns {string} Relative date in Chinese (e.g., "2天前", "1周前")
 */
export function formatDate(dateStr) {
  if (!dateStr) return 'N/A';

  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return '今天';
  if (diffDays === 1) return '昨天';
  if (diffDays < 7) return `${diffDays}天前`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}月前`;
  return `${Math.floor(diffDays / 365)}年前`;
}

/**
 * Format large numbers with compact notation
 * @param {number} num - Number to format
 * @returns {string} Formatted number (e.g., "32.5k", "1.2M")
 */
export function formatNumber(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
  return num.toString();
}
