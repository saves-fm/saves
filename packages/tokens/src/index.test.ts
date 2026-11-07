import { describe, expect, it } from 'vitest';
import { colors, fonts } from './index';

describe('tokens', () => {
  it('exposes every brand color as a hex value', () => {
    expect(colors.navy).toBe('#16205C');
    for (const value of Object.values(colors)) expect(value).toMatch(/^#[0-9A-F]{6}$/i);
  });

  it('exposes the three brand fonts', () => {
    expect(fonts).toEqual({ display: 'Pixelify Sans', body: 'Rubik', mono: 'Space Mono' });
  });
});
