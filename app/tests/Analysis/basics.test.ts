import { test, expect } from '../baseFixtures.ts';
import { deleteEverything, setupTests } from '../utils.ts';

test.beforeEach(async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('S');
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Login' }).click();
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click();
});

test.afterEach(deleteEverything);

test('file management test', async ({ page }) => {
	await page.getByRole('button', { name: 'MC02_control_head_sentence1', exact: true }).click({
		button: 'right'
	});
	await page.getByRole('menuitem', { name: 'Rename' }).click();
	await page.getByPlaceholder('MC02_control_head_sentence1').fill('renamed_file.wav');
	await page.getByPlaceholder('MC02_control_head_sentence1').press('Enter');
	await expect(
		page.getByRole('button', { name: 'MC02_control_head_sentence1', exact: true })
	).toHaveCount(0);
	await expect(page.getByRole('main')).toContainText('renamed_file.wav');
	await page.getByRole('button', { name: 'renamed_file.wav' }).click({
		button: 'right'
	});
	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('menuitem', { name: 'Download' }).click();
	const download = await downloadPromise;
	await expect(download.suggestedFilename()).toBe('renamed_file.wav');
	await page.getByRole('button', { name: 'renamed_file.wav' }).click({
		button: 'right'
	});
	await page.getByRole('menuitem', { name: 'Delete' }).click();
	await page.getByRole('button', { name: 'Continue' }).click();
	await expect(page.getByRole('button', { name: 'renamed_file.wav', exact: true })).toHaveCount(0);
	await expect(page.getByRole('textbox')).toBeVisible();
	await page.getByRole('textbox').click();
	await page
		.getByRole('textbox')
		.setInputFiles('./app/static/samples/torgo-dataset/MC02_control_head_sentence1.wav');
	await expect(page.getByRole('button', { name: 'MC02_control_head_sentence1.' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'sample' })).toBeVisible();
	await page.locator('.ml-auto').first().click();
	await expect(page.getByLabel('Are you absolutely sure?')).toBeVisible();
	await expect(page.getByLabel('Are you absolutely sure?')).toContainText(
		'This action cannot be undone. This will permanently delete this pane and the analysis conducted in it.'
	);
	await page.getByRole('button', { name: 'Continue' }).click();
	await expect(page.getByRole('button', { name: 'sample' })).toHaveCount(0);
	await page.getByRole('button', { name: 'New tab' }).click();
	await expect(page.getByRole('button', { name: 'New Tab' })).toBeVisible();
	await expect(page.getByText('Drag a file from the file')).toBeVisible();
});

//Please use chromium (firefox is used as standard) to run this test as Firefox does not support "microphone" permission
//and will throw an error Unknown permission: microphone

test('internal recorder test', async ({ page, browser }) => {
	await expect(page.getByRole('button', { name: 'new_recording' })).toHaveCount(0);
	await page.getByRole('button', { name: 'Record' }).click();
	const context = await browser.newContext();
	await context.grantPermissions(['microphone']);
	await page.waitForTimeout(1000);
	await page.getByRole('button', { name: 'Record' }).click();
	await page.locator('input[name="filename"]').click();
	await page.locator('input[name="filename"]').fill('new_recording');
	await page.locator('input[name="groundTruth"]').click();
	await page.locator('input[name="groundTruth"]').fill('hello');
	await page.getByRole('button', { name: 'Continue' }).click();
	await expect(page.getByRole('button', { name: 'new_recording' })).toBeVisible();
});
