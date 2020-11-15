import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { EvenComponent } from './even/even.component';
import { FileUploaderComponent } from './file-uploader/file-uploader.component';
import { ProgressComponent } from './file-uploader/progress/progress.component';
import { HttpClientModule } from '@angular/common/http';
import { ExistingResourcePickerComponent } from './existing-resource-picker/existing-resource-picker.component';
import { AudioComponent } from './audio/audio.component';
import { ResultsComponent } from './results/results.component';

@NgModule({
  declarations: [
    AppComponent,
    EvenComponent,
    FileUploaderComponent,
    ProgressComponent,
    ExistingResourcePickerComponent,
    AudioComponent,
    ResultsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
