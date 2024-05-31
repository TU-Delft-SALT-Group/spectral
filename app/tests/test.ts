import { test, expect } from '@playwright/test';

test('index page has expected h1', async ({ page }) => {
	await page.goto('/');
});

test('can login under sample user', async ({ page }) => {
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Start analyzing' }).click();
	await page.waitForTimeout(500);
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await page.waitForTimeout(100);
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toBeVisible();
	await expect(page.getByRole('menubar')).toContainText('home session Spectral Profile');
	await expect(page.locator('h2')).toContainText('Sample Session');
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toBeVisible();
	await expect(page.getByRole('button').first()).toBeVisible();
	await expect(page.getByRole('link', { name: 'Profile' })).toBeVisible();
});
