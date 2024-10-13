import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppController } from './app/app.component';

bootstrapApplication(AppController, appConfig)
  .catch((err) => console.error(err));
