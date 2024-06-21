import { test as teardown } from './baseFixtures.ts';
import { deleteEverything } from './utils.ts';

teardown('global teardown', deleteEverything);
