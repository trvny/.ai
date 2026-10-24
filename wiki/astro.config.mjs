import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: '.ai · Field Guide',
      description: 'A field guide to portable agent configuration, overlays and craft.',
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/trvny/.ai' }],
      sidebar: [
        { label: 'Start here', items: [
          { label: 'The Field Guide', slug: '' },
          { label: 'Design principles', slug: 'principles' },
          { label: 'Overlays and composition', slug: 'overlays' },
          { label: 'Field notes', slug: 'field-notes' },
        ] },
      ],
    }),
  ],
});
