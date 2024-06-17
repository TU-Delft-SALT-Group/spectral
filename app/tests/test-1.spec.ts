import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
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

test('test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(5) > .inline-flex').click();
	await expect(page.getByText('empty').first()).toBeVisible();
	await expect(page.getByRole('button', { name: 'Create New Track' }).first()).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('div')
			.filter({ hasText: '00.511.522.533.544.5 empty' })
			.getByRole('button')
			.nth(2)
	).toBeVisible();
	await expect(page.getByText(':00.000/00:04.800 F01_severe_head_sentence1')).toBeVisible();
});
