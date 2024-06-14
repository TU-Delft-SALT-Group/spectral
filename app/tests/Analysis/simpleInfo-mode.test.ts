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

test('simple info test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.select > .inline-flex').first().click();
	await expect(
		page.getByText('MC02_control_head_sentence1 Duration: 4.57 secondsFile size: 146 KBAverage')
	).toHaveCount(0);
	await page.locator('.select > .inline-flex').first().hover();
	await page.locator('div:nth-child(2) > .inline-flex').click();
	await page
		.getByRole('button', { name: 'MC02_control_head_sentence1' })
		.dragTo(
			page.getByText(
				'simple-info waveform spectrogram vowel-space transcription error-rate 00.511.'
			)
		);
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.select > .inline-flex').first().click();
	await expect(
		page.getByText('MC02_control_head_sentence1 Duration: 4.57 secondsFile size: 146 KBAverage')
	).toBeVisible();
	await page.locator('div:nth-child(3) > div > .inline-flex').first().click();
	await expect(
		page.getByText('MC02_control_head_sentence1 Duration: 4.57 secondsFile size: 146 KBAverage')
	).toHaveCount(0);
});

test('frame info test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.select > .inline-flex').first().click();
	await expect(page.getByText('Select a frame in the').first()).toBeVisible();
	await page.locator('.select > .inline-flex').first().hover();
	await page.locator('div:nth-child(2) > .inline-flex').first().click();
	await page.locator('canvas').first().hover();
	await page.mouse.down();
	await page.mouse.move(500, 0);
	await page.mouse.up();
	await expect(page.locator('div:nth-child(4) > div')).toBeVisible();
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('.select > .inline-flex').first().click();
	await expect(page.getByRole('heading', { name: 'Frame Duration:' })).toBeVisible();
	await expect(page.getByRole('heading', { name: 'Frame Pitch:' })).toBeVisible();
	await expect(page.getByRole('heading', { name: 'Frame F1 formant:' })).toBeVisible();
	await expect(page.getByRole('heading', { name: 'Frame F2 formant:' })).toBeVisible();
});
