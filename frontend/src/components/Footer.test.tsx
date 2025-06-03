import { render, screen } from '@testing-library/react';
import Footer from './Footer';

test('renders copyright notice', () => {
  render(<Footer />);
  expect(screen.getByText(/Aurianne Swchartz & Léopold Chappuis/i)).toBeInTheDocument();
});
