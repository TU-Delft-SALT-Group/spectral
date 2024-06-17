import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*{test,spec}.{js,ts}']
	},
	build: {
		target: 'ES2022'
	},
	esbuild: {
		target: 'esnext'
	}
});
