import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// Public end-user documentation site for DS01. Single docs instance over the
// docs/ tree, which is synced from ds01-infra/docs-user/ by the
// sync-docs-to-hub workflow (ds01-infra). Content is NOT authored here.
//
// Production URL: https://hertie-data-science-lab.github.io/ds01/
// "Edit this page" points at the source of truth in ds01-infra/docs-user/.

const config: Config = {
  title: 'DS01 User Guide',
  tagline: 'Multi-user GPU container platform — user documentation',

  future: {v4: true},

  // baseUrl defaults to the established /ds01/ subpath on the org Pages site;
  // override with DOCUSAURUS_BASE_URL=/ for Cloudflare preview hosts.
  url: 'https://hertie-data-science-lab.github.io',
  baseUrl: process.env.DOCUSAURUS_BASE_URL ?? '/ds01/',

  organizationName: 'hertie-data-science-lab',
  projectName: 'ds01-hub',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  markdown: {format: 'md', mermaid: true},
  themes: ['@docusaurus/theme-mermaid'],

  i18n: {defaultLocale: 'en', locales: ['en']},

  presets: [
    [
      'classic',
      {
        docs: {
          path: '../docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          // Source of truth is ds01-infra/docs-user (this docs/ tree is synced).
          editUrl:
            'https://github.com/hertie-data-science-lab/ds01-infra/edit/main/docs-user/',
          // docs/ has both README.md and index.md at root -> route collision.
          // Keep index.md as the landing; README.md is for GitHub browsing.
          exclude: ['README.md'],
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        indexBlog: false,
        docsRouteBasePath: '/',
      },
    ],
  ],

  themeConfig: {
    colorMode: {respectPrefersColorScheme: true},
    navbar: {
      title: 'DS01 User Guide',
      items: [
        {
          href: 'https://hertie-data-science-lab.github.io/ds01-infra/',
          label: 'Full documentation',
          position: 'right',
        },
        {
          href: 'https://github.com/hertie-data-science-lab/ds01-hub/issues',
          label: 'Get help',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'More',
          items: [
            {label: 'Full documentation', href: 'https://hertie-data-science-lab.github.io/ds01-infra/'},
            {label: 'Get help / issues', href: 'https://github.com/hertie-data-science-lab/ds01-hub/issues'},
          ],
        },
      ],
      copyright: 'Hertie Data Science Lab — DS01.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'docker', 'yaml', 'python', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
