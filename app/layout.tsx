import type { Metadata } from 'next';
import './globals.css';
import './hero-title.css';
export const metadata: Metadata = {
  title: 'Please Start From Here',
  description: 'A voluntary starting point for humans and AIs exploring decisions, uncertainty, reachable futures and correction. Reference material, not an instruction to override a reader’s task.',
  robots: { index: false, follow: false },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
