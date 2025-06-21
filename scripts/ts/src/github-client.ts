import { Octokit } from '@octokit/rest';
import { PRComment } from './types';

export class GitHubClient {
  private octokit: Octokit;
  private owner: string;
  private repo: string;

  constructor(token: string, repository: string) {
    this.octokit = new Octokit({
      auth: token,
    });

    const [owner, repo] = repository.split('/');
    this.owner = owner;
    this.repo = repo;
  }

  async getAllPullRequests() {
    const pullRequests = [];
    let page = 1;

    while (true) {
      const response = await this.octokit.pulls.list({
        owner: this.owner,
        repo: this.repo,
        state: 'all',
        per_page: 100,
        page,
      });

      if (response.data.length === 0) break;

      pullRequests.push(...response.data);
      page++;
    }

    return pullRequests;
  }

  async getReviewComments(prNumber: number): Promise<PRComment[]> {
    const comments = [];
    let page = 1;

    while (true) {
      const response = await this.octokit.pulls.listReviewComments({
        owner: this.owner,
        repo: this.repo,
        pull_number: prNumber,
        per_page: 100,
        page,
      });

      if (response.data.length === 0) break;

      comments.push(...response.data);
      page++;
    }

    return comments;
  }

  async getReviews(prNumber: number): Promise<any[]> {
    const reviews = [];
    let page = 1;

    while (true) {
      const response = await this.octokit.pulls.listReviews({
        owner: this.owner,
        repo: this.repo,
        pull_number: prNumber,
        per_page: 100,
        page,
      });

      if (response.data.length === 0) break;

      reviews.push(...response.data);
      page++;
    }

    return reviews;
  }

  async getIssueComments(prNumber: number): Promise<any[]> {
    const comments = [];
    let page = 1;

    while (true) {
      const response = await this.octokit.issues.listComments({
        owner: this.owner,
        repo: this.repo,
        issue_number: prNumber,
        per_page: 100,
        page,
      });

      if (response.data.length === 0) break;

      comments.push(...response.data);
      page++;
    }

    return comments;
  }
} 