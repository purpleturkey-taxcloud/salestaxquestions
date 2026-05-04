import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const questions = await getCollection('questions');

  const byTopic = questions
    .filter(q => q.data.slug && q.data.slug !== 'homepage')
    .reduce((acc, q) => {
      const topic = q.data.topic ?? 'General';
      if (!acc[topic]) acc[topic] = [];
      acc[topic].push(q);
      return acc;
    }, {} as Record<string, typeof questions>);

  const lines: string[] = [
    '# Sales Tax Questions',
    '',
    '> Plain-language answers to U.S. sales tax questions for ecommerce businesses. Covers economic nexus, physical nexus, product taxability, exemption certificates, marketplace facilitators, filing deadlines, audits, state guides, and software comparisons. Content is written for founders, finance teams, and controllers — not lawyers.',
    '',
    '## Pages',
    '',
    '- [Home](https://salestaxquestions.com/): Overview and topic directory',
    '- [Topics](https://salestaxquestions.com/topics/): All 15 topic categories',
    '- [States](https://salestaxquestions.com/states/): Sales tax guide for every U.S. state',
    '- [Compare](https://salestaxquestions.com/compare/): Sales tax software comparisons',
    '',
  ];

  for (const [topic, qs] of Object.entries(byTopic).sort()) {
    lines.push(`## ${topic}`);
    lines.push('');
    for (const q of qs.sort((a, b) => a.data.title.localeCompare(b.data.title))) {
      const desc = q.data.metaDescription ? ` — ${q.data.metaDescription}` : '';
      lines.push(`- [${q.data.title}](https://salestaxquestions.com/${q.data.slug}/)${desc}`);
    }
    lines.push('');
  }

  return new Response(lines.join('\n'), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
