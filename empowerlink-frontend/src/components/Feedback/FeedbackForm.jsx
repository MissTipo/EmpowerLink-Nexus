import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';

const SUBMIT_FEEDBACK = gql`
  mutation SubmitFeedback($input: FeedbackInput!) {
    submitFeedback(input: $input) {
      success
      message
    }
  }
`;

export default function FeedbackForm() {
  const [comment, setComment] = useState('');
  const [reportType, setReportType] = useState('COMMENT');
  const [submitFeedback, { loading, error, data }] = useMutation(SUBMIT_FEEDBACK);

  const handleSubmit = async e => {
    e.preventDefault();
    await submitFeedback({ variables: { input: { type: reportType, content: comment } } });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block mb-1">Type</label>
        <select value={reportType} onChange={e => setReportType(e.target.value)} className="w-full p-2 border rounded">
          <option value="COMMENT">Comment</option>
          <option value="REPORT">Report</option>
        </select>
      </div>
      <div>
        <label className="block mb-1">Your Feedback</label>
        <textarea
          value={comment}
          onChange={e => setComment(e.target.value)}
          rows={4}
          className="w-full p-2 border rounded"
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-teal-600 text-white rounded"
      >
        {loading ? 'Submitting...' : 'Submit'}
      </button>
      {error && <p className="text-red-500">Error submitting feedback</p>}
      {data?.submitFeedback.success && <p className="text-green-600">{data.submitFeedback.message}</p>}
    </form>
  );
}
