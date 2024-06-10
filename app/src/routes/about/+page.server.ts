import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeDocument from 'rehype-document';
import rehypeFormat from 'rehype-format';
import rehypeStringify from 'rehype-stringify';
import { read } from 'to-vfile';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const markDown = await unified()
		.use(remarkParse)
		.use(remarkRehype)
		.use(rehypeDocument)
		.use(rehypeFormat)
		.use(rehypeStringify)
		.process(await read('src/routes/about/about.md'));

	return { markDown: markDown.toString() };
};

export const prerender = true;
