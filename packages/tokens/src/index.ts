// Design tokens for the web and mobile apps. The source is brand/tokens.json;
// v0.2.0 adds the build that generates CSS variables and a Dart theme from it
// (with contrast checks), so neither app hardcodes a value.
import brand from '../../../brand/tokens.json';

export type ColorToken = keyof typeof brand.color;

export const colors = Object.fromEntries(
  Object.entries(brand.color).map(([name, token]) => [name, token.value]),
) as Record<ColorToken, string>;

export const fonts = {
  display: brand.font.display.family,
  body: brand.font.body.family,
  mono: brand.font.mono.family,
};
