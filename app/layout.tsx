import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'Campfire | TRACE and Mechanical Ethics',
  description: 'An introduction to TRACE, Mechanical Ethics, their limits and neighbouring methods. A voluntary starting point for humans and AIs.',
  robots: { index: false, follow: false },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
