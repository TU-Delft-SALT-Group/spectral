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

test('playback test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.main > div:nth-child(3) > .inline-flex').click();
	await expect(page.locator('canvas:nth-child(2)').first()).toBeVisible();
	await expect(
		page.locator(
			'section:nth-child(2) > div > div > .waveform > div > .scroll > .wrapper > div:nth-child(5) > canvas:nth-child(2)'
		)
	).toBeVisible();
	await expect(page.getByRole('group')).toContainText('00:00.000/00:04.800');
	await expect(page.getByRole('group')).toContainText('1.00x');
	await page.getByText('1.00x').first().click();
	await page.getByRole('option', { name: '1.50x' }).click();
	await expect(page.getByRole('group')).toContainText('1.50x');
	await page
		.getByRole('group')
		.locator('section')
		.filter({
			hasText: '00:00.000/00:04.800 1.50x F01_severe_head_sentence1 00:00.000/00:03.404 1.00x'
		})
		.getByRole('button')
		.first()
		.click();
	await expect(page.getByText('00:00.000/00:04.800')).toHaveCount(0);
	await page.locator('canvas:nth-child(2)').first().click();
	await expect(page.getByRole('group')).toContainText('00:02.398/00:04.800');
});

test('drag and drop test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.main > div:nth-child(3) > .inline-flex').click();
	await expect(page.getByText('00:00.000/00:04.565 1.00x')).toHaveCount(0);
	await page
		.getByRole('button', { name: 'MC02_control_head_sentence1' })
		.dragTo(
			page.getByText(
				'00:00.000/00:04.800 1.00x F01_severe_head_sentence1 00:00.000/00:03.404 1.00x'
			)
		);
	await expect(page.getByText('00:00.000/00:04.565 1.00x')).toBeVisible();
});

test.afterEach(async ({ page }) => {
	await page.close();
});
