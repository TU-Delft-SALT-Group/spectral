import { test, expect } from '../baseFixtures.ts';
import { deleteEverything, setupTests } from '../utils.ts';

test.beforeEach(async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('S');
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click();
});

test.afterEach(deleteEverything);

test('vowel space test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(4) > .inline-flex').click();
	await expect(
		page.getByText('2,0001,8001,6001,4001,2001,0008006004002000F2 - F12,8002,6002,4002,2002,0001,')
	).toBeVisible();
	await expect(page.getByRole('group')).toContainText('F2 - F1');
	await expect(page.locator('label')).toContainText('Show legend');
	await expect(page.getByTitle('F01_severe_head_sentence1')).toHaveCount(0);
	await expect(page.getByTitle('F03_moderate_head_sentence1')).toHaveCount(0);
	await page.locator('div:nth-child(4) > .inline-flex').hover();
	await page.locator('div:nth-child(2) > .inline-flex').click();
	await page.locator('canvas').first().hover();
	await page.mouse.down();
	await page.mouse.move(500, 0);
	await page.mouse.up();
	await page.locator('canvas').nth(2).hover();
	await page.mouse.down();
	await page.mouse.move(500, 0);
	await page.mouse.up();
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(4) > .inline-flex').click();
	await expect(page.getByTitle('F01_severe_head_sentence1')).toBeVisible();
	await expect(page.getByTitle('F03_moderate_head_sentence1')).toBeVisible();
	await expect(
		page.locator('svg').filter({ hasText: '2,0001,8001,6001,4001,2001,' }).locator('circle').first()
	).toBeVisible();
	await expect(
		page.locator('svg').filter({ hasText: '2,0001,8001,6001,4001,2001,' }).locator('circle').nth(1)
	).toBeVisible();
});
