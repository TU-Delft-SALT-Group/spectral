import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
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
	await page.goto('http://localhost/session/sample-session');
	await page.getByRole('button', { name: 'MC02_control_head_sentence1', exact: true }).click({
		button: 'right'
	});
	await page.locator('div:nth-child(23) > div').first().click();
	await page.getByPlaceholder('MC02_control_head_sentence1').fill('renamed_file');
	await page.getByPlaceholder('MC02_control_head_sentence1').press('Enter');
	await expect(
		page.getByRole('button', { name: 'MC02_control_head_sentence1', exact: true })
	).toHaveCount(0);
	await expect(page.getByRole('main')).toContainText('renamed_file');
	await page.getByRole('button', { name: 'renamed_file' }).click({
		button: 'right'
	});
	await page.locator('div:nth-child(23) > div:nth-child(3)').click();
	await page.getByRole('button', { name: 'Continue' }).click();
	await expect(page.getByRole('button', { name: 'renamed_file', exact: true })).toHaveCount(0);
	await expect(page.getByRole('textbox')).toBeVisible();
	await page.getByRole('textbox').click();
	await page
		.getByRole('textbox')
		.setInputFiles('./app/static/samples/torgo-dataset/MC02_control_head_sentence1.wav');
	await expect(page.getByRole('button', { name: 'MC02_control_head_sentence1.' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'sample' })).toBeVisible();
	await page
		.locator('div')
		.filter({ hasText: /^sample \+$/ })
		.getByRole('button')
		.nth(1)
		.click();
	await expect(page.getByRole('button', { name: 'sample' })).toHaveCount(0);
	await page.getByRole('button', { name: 'New tab' }).click();
	await expect(page.getByRole('button', { name: 'default' })).toBeVisible();
});
