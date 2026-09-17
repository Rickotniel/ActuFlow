import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { addIcons } from 'ionicons';
import {
  alertCircleOutline,
  addOutline,
  arrowForwardOutline,
  bookOutline,
  briefcaseOutline,
  calendarOutline,
  closeOutline,
  createOutline,
  eyeOutline,
  happyOutline,
  heart,
  heartOutline,
  homeOutline,
  logInOutline,
  logOutOutline,
  newspaperOutline,
  personAddOutline,
  personCircleOutline
} from 'ionicons/icons';

addIcons({
  alertCircleOutline,
  addOutline,
  arrowForwardOutline,
  bookOutline,
  briefcaseOutline,
  calendarOutline,
  closeOutline,
  createOutline,
  eyeOutline,
  happyOutline,
  heart,
  heartOutline,
  homeOutline,
  logInOutline,
  logOutOutline,
  newspaperOutline,
  personAddOutline,
  personCircleOutline
});

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.log(err));
