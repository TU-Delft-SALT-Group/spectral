import { PlaywrightTestConfig, devices } from '@playwright/test';

const config: PlaywrightTestConfig = {
	webServer: {
		command: 'docker compose up --build', // or 'docker run -p 80:80 my-web-app'
		url: 'http://localhost:80',
		timeout: 600 * 1000,
		reuseExistingServer: !process.env.CI
	},
	projects: [
		{
			name: 'setup account',
			testMatch: /global\.setup\.ts/
		},
		{
			name: 'chromium',
			use: { ...devices['Desktop Chrome'] },
			dependencies: ['setup account']
		},
		{
			name: 'firefox',
			use: { ...devices['Desktop Firefox'] },
			dependencies: ['setup account']
		}
	],
	use: {
		baseURL: 'http://localhost:80'
	},
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/
};

export default config;
