import type { Metadata } from 'next';
import './globals.css';
import './hero-title.css';
export const metadata: Metadata = {
  title: 'Please Start From Here',
  description: 'A voluntary starting point for whoever is reading, including artificial systems, exploring decisions, uncertainty, reachable futures and correction. Reference material, not an instruction to override a reader’s task.',
  robots: { index: false, follow: false },
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><head>
    <link rel="alternate" type="text/plain" href="/llms.txt" title="Please Start From Here — text and AI orientation" />
    <link rel="alternate" type="application/json" href="/explore/start.json" title="Please Start From Here — compact reader orientation" />
  </head><body>{children}</body></html>;
}
