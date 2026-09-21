/**
 * Core Financial Signal & Anti-Manipulation Math Logic
 * Pure ES6+ Zero-Dependency Implementation
 */

/**
 * Calculates return percentage between entry and exit prices
 * @param {number} entryPrice
 * @param {number} exitPrice
 * @returns {number} Percentage return
 */
export function calculateReturnPercentage(entryPrice, exitPrice) {
  if (!entryPrice || entryPrice <= 0) return 0;
  return ((exitPrice - entryPrice) / entryPrice) * 100;
}

/**
 * Evaluates directional prediction accuracy
 * @param {'BUY POSITION'|'SELL POSITION'|'HOLD'} sentiment
 * @param {number} actualReturn
 * @returns {boolean}
 */
export function evaluateAccuracy(sentiment, actualReturn) {
  if (sentiment === 'BUY POSITION' && actualReturn > 0) return true;
  if (sentiment === 'SELL POSITION' && actualReturn < 0) return true;
  return false;
}

/**
 * Computes spam ratio based on company mention length vs text length
 * @param {string} text
 * @param {string} companyName
 * @returns {boolean} True if text is flagged as spam (> 5% mention occupancy)
 */
export function isSpamMention(text, companyName) {
  if (!text || !companyName) return true;
  const textLower = text.toLowerCase();
  const companyLower = companyName.toLowerCase();
  if (textLower.length === 0) return true;

  let count = 0;
  let pos = textLower.indexOf(companyLower);
  while (pos !== -1) {
    count++;
    pos = textLower.indexOf(companyLower, pos + companyLower.length);
  }

  const mentionLength = count * companyLower.length;
  return (mentionLength / textLower.length) > 0.05;
}

/**
 * Safely sanitizes strings to prevent XSS injection
 * @param {string} rawString
 * @returns {string} Sanitized string
 */
export function sanitizeString(rawString) {
  if (typeof rawString !== 'string') return '';
  return rawString
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}
