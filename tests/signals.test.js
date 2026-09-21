import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  calculateReturnPercentage,
  evaluateAccuracy,
  isSpamMention,
  sanitizeString,
} from '../frontend/src/utils/signals.js';

describe('Financial Signals & Business Logic Suite', () => {
  describe('calculateReturnPercentage', () => {
    it('accurately calculates positive gains', () => {
      const res = calculateReturnPercentage(100, 105);
      assert.equal(res, 5);
    });

    it('accurately calculates negative drawdowns', () => {
      const res = calculateReturnPercentage(200, 190);
      assert.equal(res, -5);
    });

    it('safely handles zero or invalid entry price', () => {
      assert.equal(calculateReturnPercentage(0, 100), 0);
      assert.equal(calculateReturnPercentage(-10, 100), 0);
    });
  });

  describe('evaluateAccuracy', () => {
    it('marks BUY POSITION with positive return as accurate', () => {
      assert.equal(evaluateAccuracy('BUY POSITION', 1.25), true);
      assert.equal(evaluateAccuracy('BUY POSITION', -0.5), false);
    });

    it('marks SELL POSITION with negative return as accurate', () => {
      assert.equal(evaluateAccuracy('SELL POSITION', -2.1), true);
      assert.equal(evaluateAccuracy('SELL POSITION', 0.8), false);
    });

    it('marks HOLD or zero return as non-directional accurate', () => {
      assert.equal(evaluateAccuracy('HOLD', 1.5), false);
      assert.equal(evaluateAccuracy('BUY POSITION', 0), false);
    });
  });

  describe('Anti-Manipulation & Spam Detection', () => {
    it('flags text when company name occupies > 5% of content', () => {
      const company = 'Reliance';
      const text = 'Reliance Reliance Reliance stock update today.';
      assert.equal(isSpamMention(text, company), true);
    });

    it('passes legitimate headlines where mention is < 5%', () => {
      const company = 'Tata';
      const text =
        'Major economic reforms announced by central financial authorities impacting commercial transport and manufacturing including Tata across national industrial corridors.';
      assert.equal(isSpamMention(text, company), false);
    });
  });

  describe('Sanitization & XSS Safety', () => {
    it('escapes dangerous HTML characters', () => {
      const malicious = '<script>alert("xss")</script>';
      const clean = sanitizeString(malicious);
      assert.equal(clean, '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;');
      assert.ok(!clean.includes('<script>'));
    });

    it('handles empty or non-string inputs safely', () => {
      assert.equal(sanitizeString(null), '');
      assert.equal(sanitizeString(undefined), '');
      assert.equal(sanitizeString(12345), '');
    });
  });
});
