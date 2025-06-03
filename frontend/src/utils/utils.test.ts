import getBaseURL from './utils';

describe('getBaseURL', () => {
  const originalLocation = window.location;

  beforeAll(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { protocol: 'https:', hostname: 'example.com', port: '3000' },
    } as any);
  });

  afterAll(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: originalLocation,
    });
  });

  it('returns the base url built from window.location', () => {
    expect(getBaseURL()).toBe('https://example.com:3000');
  });
});
