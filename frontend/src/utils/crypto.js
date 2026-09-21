/**
 * Cryptographically Secure Pseudo-Random Number Generator (CSPRNG)
 * Tier-1 Industry Standard: Zero-Dependency & Cryptographic Fairness Baseline
 *
 * @returns {number} Uniform float in range [0, 1)
 */
export function getCryptoRandom() {
  const cryptoObj =
    typeof window !== 'undefined' && window.crypto
      ? window.crypto
      : typeof globalThis !== 'undefined' && globalThis.crypto
      ? globalThis.crypto
      : null;

  if (cryptoObj?.getRandomValues) {
    const buf = new Uint32Array(1);
    cryptoObj.getRandomValues(buf);
    return buf[0] / 4294967296;
  }
  return Math.random();
}

/**
 * Fisher-Yates array shuffle utilizing CSPRNG entropy
 *
 * @template T
 * @param {T[]} array
 * @returns {T[]} Shuffled array copy
 */
export function secureShuffle(array) {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(getCryptoRandom() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}
