import { readFile } from 'node:fs/promises';
import { db } from '.';
import { fileTable, sessionTable, userTable } from './schema';
import { eq } from 'drizzle-orm';
import type { SessionState } from '../../routes/(protected)/session/[sessionId]/workspace';
import { createUser } from './users';

const sampleTorgo = [
	'F01_severe_head_sentence1',
	'F03_moderate_head_sentence1',
	'FC03_control_head_sentence1',
	'M02_severe_head_sentence1',
	'M03_mild_head_sentence1',
	'M04_severe_head_sentence1',
	'MC02_control_head_sentence1'
];

const sampleUser = {
	id: 'sample-user',
	username: 'Sample',
	email: 'sample@example.com',
	password: 'password',
	privacyAck: true
};

export async function seedSampleUser() {
	const isSampleUserSeeded = await db.query.userTable.findFirst({
		where: eq(userTable.id, sampleUser.id)
	});

	if (!isSampleUserSeeded) {
		await createUser(sampleUser);
	}

	return { isSampleUserSeeded };
}

const sampleSessionState: SessionState = {
	panes: {
		'sample-session-id': {
			title: 'sample',
			mode: 'waveform',
			files: [
				{
					id: sampleTorgo[0],
					name: sampleTorgo[0],
					frame: null,
					cycleEnabled: false,
					transcriptions: [],
					groundTruth: 'the quick brown fox jumps over the lazy dog',
					note: 'from Torgo dataset',
					reference: null,
					hypothesis: null
				},

				{
					id: sampleTorgo[1],
					name: sampleTorgo[1],
					frame: null,
					cycleEnabled: true,
					transcriptions: [],
					groundTruth: 'the quick brown fox jumps over the lazy dog',
					note: 'from Torgo dataset',
					reference: null,
					hypothesis: null
				}
			],

			modeState: {
				'simple-info': {},
				waveform: { width: 100 },
				spectrogram: { width: 100 },
				transcription: {},
				'vowel-space': {
					showLegend: true
				},
				'error-rate': {}
			}
		}
	}
};
const sampleSession = {
	id: 'sample-session',
	name: 'Sample Session',
	owner: sampleUser.id,
	state: sampleSessionState
};

export async function seedSampleSession() {
	const { isSampleUserSeeded } = await seedSampleUser();

	const isSampleSessionSeeded = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, 'sample-session')
	});

	if (!isSampleSessionSeeded) {
		await db.insert(sessionTable).values(sampleSession);
	}

	return { isSampleUserSeeded, isSampleSessionSeeded };
}

export async function seedSampleTorgo() {
	const { isSampleUserSeeded, isSampleSessionSeeded } = await seedSampleSession();

	for (const filename of sampleTorgo) {
		const isFileSeeded = await db.query.fileTable.findFirst({
			where: eq(fileTable.id, filename)
		});

		if (isFileSeeded) {
			continue;
		}

		const buffer = await readFile(`./static/samples/torgo-dataset/${filename}.wav`);

		await db.insert(fileTable).values({
			id: filename,
			name: filename,
			session: sampleSession.id,
			data: buffer,
			uploader: sampleUser.id,
			groundTruth: 'the quick brown fox jumps over the lazy dog'
		});
	}

	return { isSampleUserSeeded, isSampleSessionSeeded, isSampleTorgoSeeded: true };
}
