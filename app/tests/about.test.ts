import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'About' }).click();
	await expect(page.getByRole('link', { name: 'about' })).toBeVisible();
	await expect(page.locator('body')).toContainText('About Spectral');
	await expect(page.getByText('In 2024, we were tasked by')).toBeVisible();
	await expect(page.locator('body')).toContainText('About Us');
});

test.afterEach(async ({ page }) => {
	await page.close();
});
