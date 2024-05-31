import { test, expect } from '@playwright/test';

test('everything in session is visible', async ({ page }) => {
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Start analyzing' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click();
	await expect(page.locator('canvas').first()).toBeVisible();
	await expect(page.locator('canvas').nth(2)).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00:00.000/00:04.800 1.00x F01_severe_head_sentence1 00:00.000/00:03.404 1.00x'
			})
			.getByRole('button')
			.first()
	).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00:00.000/00:04.800 1.00x F01_severe_head_sentence1 00:00.000/00:03.404 1.00x'
			})
			.getByRole('button')
			.nth(1)
	).toBeVisible();
	await expect(page.locator('li').filter({ hasText: 'F01_severe_head_sentence1' })).toBeVisible();
	await expect(page.locator('li').filter({ hasText: 'F03_moderate_head_sentence1' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'MC02_control_head_sentence1' })).toBeVisible();
	await expect(page.getByText('home session sample-session Spectral Profile')).toBeVisible();
	await expect(page.getByRole('button', { name: 'Record' })).toBeVisible();
	await expect(page.getByRole('textbox')).toBeVisible();
	await expect(page.getByText('1.00x').first()).toBeVisible();
	await expect(page.getByText('1.00x').nth(1)).toBeVisible();
});
