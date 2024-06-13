import { test, expect } from '@playwright/test';

test('waveform test', async ({ page }) => {
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
	await expect(page.getByRole('group')).toContainText('1.00x');
	await page.getByText('1.00x').first().click();
	await page.getByRole('option', { name: '1.50x' }).click();
	await expect(page.getByRole('group')).toContainText('1.50x');
	await expect(page.getByText('00:00.000/00:04.800')).toBeVisible();
	await page
		.getByRole('group')
		.locator('section')
		.filter({
			hasText: '00.511.522.533.544.5 00:00.000/00:04.800 1.50x F01_severe_head_sentence1 00.511'
		})
		.getByRole('button')
		.first()
		.click();
	await expect(page.getByText('00:00.000/00:04.800')).toHaveCount(0);
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00.511.522.533.544.5 00:04.831/00:04.800 1.50x F01_severe_head_sentence1 00.511'
			})
			.getByRole('button')
			.nth(2)
	).toHaveCount(0);
	await page
		.getByRole('button', { name: 'MC02_control_head_sentence1' })
		.dragTo(
			page.getByText(
				'simple-info waveform spectrogram vowel-space transcription error-rate 00.511.'
			)
		);
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00.511.522.533.544.5 00:04.831/00:04.800 1.50x F01_severe_head_sentence1 00.511'
			})
			.getByRole('button')
			.nth(2)
	).toBeVisible;
});
