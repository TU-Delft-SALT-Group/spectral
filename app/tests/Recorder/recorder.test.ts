import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Record' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('S');
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await page.waitForTimeout(1000);
	await page.getByRole('textbox').click();
	await page.getByRole('textbox').setInputFiles('./app/static/samples/prompts/text-7.txt');
});

//Please use chromium (firefox is used as standard) to run this test file as Firefox does not support "microphone" permission
//and will throw an error Unknown permission: microphone

test('test', async ({ page, browser }) => {
	const context = await browser.newContext();
	await context.grantPermissions(['microphone', 'camera']);
	await page.waitForTimeout(5000);
	await expect(page.getByText('You have recorded 0/7 prompts')).toBeVisible();
	await expect(page.getByRole('button', { name: 'Export recording to session' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'Save files to disk' })).toBeVisible();
	await expect(page.getByRole('heading', { name: 'until missus bofin announced' })).toBeVisible();
	await expect(
		page.locator('section').filter({ hasText: 'until missus bofin announced' }).locator('video')
	).toBeVisible();
	await page.getByRole('button', { name: 'Record', exact: true }).first().click();
	await page.waitForTimeout(1000);
	await page.getByRole('button', { name: 'Stop recording' }).first().click();
	await expect(page.getByRole('button', { name: 'Take' })).toBeVisible();
	await expect(
		page.locator('li').filter({ hasText: 'Take' }).getByRole('button').nth(1)
	).toBeVisible();
	await page.locator('li').filter({ hasText: 'Take' }).getByRole('button').nth(1).click();
	await page.getByRole('button', { name: 'Record', exact: true }).first().click();
	await page.getByRole('button', { name: 'Stop recording' }).first().click();
	await expect(page.getByText('You have recorded 1/7 prompts')).toBeVisible();
	await page.getByRole('button', { name: 'Record', exact: true }).first().click();
	await page.waitForTimeout(1000);
	await page.getByRole('button', { name: 'Stop recording' }).first().click();
	await page.getByRole('button', { name: 'Record', exact: true }).first().click();
	await page.waitForTimeout(1000);
	await page.getByRole('button', { name: 'Stop recording' }).first().click();
	await page.getByRole('button', { name: 'Take 2' }).click();
	await expect(page.getByText('Notes for take')).toBeVisible();
	await page.getByRole('textbox').click();
	await page.getByRole('textbox').press('CapsLock');
	await page.getByRole('textbox').fill('S');
	await page.getByRole('textbox').press('CapsLock');
	await page.getByRole('textbox').fill('Some notes');
	await page.getByRole('button', { name: 'Take 2' }).click();
	await page.getByRole('button', { name: 'Take 1' }).click();
	await expect(page.getByText('Notes for take')).toBeVisible();
	await expect(page.getByRole('textbox')).toContainText('');
	await page.getByRole('button', { name: 'Take 3' }).click();
	await expect(page.getByText('Notes for take')).toBeVisible();
	await expect(page.getByRole('textbox')).toContainText('');
	await page.getByRole('button', { name: 'Take 3' }).click();
	await page.locator('li').filter({ hasText: 'Take 3' }).getByRole('button').nth(1).click();
	await page.locator('button:nth-child(3)').first().click();
	await page.getByRole('button', { name: 'Record', exact: true }).nth(1).click();
	await page.waitForTimeout(1000);
	await page.getByRole('button', { name: 'Stop recording' }).nth(1).click();
	await expect(page.getByRole('button', { name: 'Take' }).nth(2)).toBeVisible();
	await expect(page.getByText('You have recorded 2/7 prompts')).toBeVisible();
	await page
		.locator('section')
		.filter({ hasText: 'you know it inquired bryce 2' })
		.getByRole('button')
		.nth(1)
		.click();
	await expect(page.getByRole('button', { name: 'Take' }).first()).toBeVisible();
	await expect(page.getByRole('button', { name: 'Take 2' })).toBeVisible();
});
