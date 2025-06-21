export interface PRComment {
  pr_number: number;
  pr_title: string;
  pr_state: string;
  pr_created_at: string;
  pr_merged_at: string;
  pr_author: string;
  comment_type: 'review_comment' | 'review' | 'issue_comment';
  comment_id: number;
  comment_body: string;
  comment_created_at: string;
  comment_updated_at: string;
  comment_user: string;
  comment_path: string;
  comment_line: number | null;
  comment_side: string;
  comment_start_line: number | null;
  comment_start_side: string;
}

export interface CommentSummary {
  total_comments: number;
  total_prs: number;
  comment_types: Record<string, number>;
  users: Record<string, number>;
  generated_at: string;
}

export interface CommentListResult {
  summary: CommentSummary;
  comments: PRComment[];
}

export interface CommentCounts {
  total_prs: number;
  total_comments: number;
  review_comments: number;
  reviews: number;
  issue_comments: number;
  avg_comments_per_pr: number;
  prs_with_comments: number;
  prs_without_comments: number;
} 