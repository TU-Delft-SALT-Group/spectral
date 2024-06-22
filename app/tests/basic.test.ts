import { test } from './baseFixtures.ts';
import { deleteEverything, setupTests } from './utils.ts';

test('index page has expected h1', async ({ page }) => {
	await setupTests({ page });
	await page.goto('/');
});

test.afterEach(deleteEverything);
