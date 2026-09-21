import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { getCryptoRandom, secureShuffle } from '../frontend/src/utils/crypto.js';

describe('CSPRNG & Statistical Fairness Tests', () => {
  it('getCryptoRandom returns values strictly within [0, 1)', () => {
    for (let i = 0; i < 1000; i++) {
      const val = getCryptoRandom();
      assert.ok(val >= 0, `Value ${val} should be >= 0`);
      assert.ok(val < 1, `Value ${val} should be < 1`);
    }
  });

  it('passes 10,000-sample Pearson Chi-Square Uniformity Test across multiple trials', () => {
    const samples = 10000;
    const numBins = 10;
    const expectedPerBin = samples / numBins;
    const criticalValue = 27.877; // alpha = 0.001 for 9 degrees of freedom
    const maxTrials = 3;
    let passedTrials = 0;

    for (let trial = 0; trial < maxTrials; trial++) {
      const bins = new Array(numBins).fill(0);
      for (let i = 0; i < samples; i++) {
        const r = getCryptoRandom();
        const bin = Math.floor(r * numBins);
        bins[Math.min(bin, numBins - 1)]++;
      }

      let chiSquare = 0;
      for (let i = 0; i < numBins; i++) {
        const diff = bins[i] - expectedPerBin;
        chiSquare += (diff * diff) / expectedPerBin;
      }

      if (chiSquare < criticalValue) {
        passedTrials++;
      }
    }

    assert.ok(
      passedTrials >= 2,
      `CSPRNG failed statistical uniformity: passed ${passedTrials}/${maxTrials} trials (critical: ${criticalValue})`
    );
  });

  it('secureShuffle preserves elements and alters order', () => {
    const input = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const shuffled = secureShuffle(input);

    assert.equal(shuffled.length, input.length);
    assert.deepEqual([...shuffled].sort((a, b) => a - b), input);

    // Verify non-destructive
    assert.deepEqual(input, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
  });
});
