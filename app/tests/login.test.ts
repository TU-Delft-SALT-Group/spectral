import { test, expect } from './baseFixtures.ts';
import { deleteEverything, setupTests } from './utils.ts';

test('can login under sample user', async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toBeVisible();
	await expect(page.getByRole('menubar')).toContainText('home session Spectral Profile');
	await expect(page.locator('h2')).toContainText('Sample Session');
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toBeVisible();
	await expect(page.getByRole('button').first()).toBeVisible();
	await expect(page.getByRole('link', { name: 'Profile' })).toBeVisible();
});

test('invalid username or password', async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Spectral');
	await page.getByLabel('Username').press('Tab');
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await expect(page.locator('form')).toContainText('Invalid username or password');
});

test.afterEach(deleteEverything);
