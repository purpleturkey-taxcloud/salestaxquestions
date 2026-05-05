import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const questions = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/questions' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    topic: z.string().optional(),
    topicSlug: z.string().optional(),
    type: z.string().optional(),
    difficulty: z.string().optional(),
    publishedAt: z.string().optional(),
    updatedAt: z.string().optional(),
    related: z.array(z.string()).optional(),
    metaDescription: z.string().optional(),
    tldr: z.string().optional(),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
  }),
});

export const collections = { questions };
