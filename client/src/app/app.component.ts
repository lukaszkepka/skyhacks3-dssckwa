import { HttpClient, HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { pipe } from 'rxjs';
import { filter, map, tap } from 'rxjs/operators';
import { LabelByPeriods } from "./audio/audio.component";
import { FileUploaderComponent } from './file-uploader/file-uploader.component';
import { requiredFileType } from './upload-file-validators';

export function uploadProgress<T>( cb: ( progress: number ) => void ) {
  return tap(( event: HttpEvent<T> ) => {
    if ( event.type === HttpEventType.UploadProgress ) {
      cb(Math.round((100 * event.loaded) / event.total));
    }
  });
}

export function toResponseBody<T>() {
  return pipe(
    filter(( event: HttpEvent<T> ) => event.type === HttpEventType.Response),
    map(( res: HttpResponse<T> ) => res.body)
  );
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  @ViewChild(FileUploaderComponent) fileUploaderComponent: FileUploaderComponent;

  progress = 0;
  userMediaUrl: string;
  showUserMedia: boolean;
  userMediaResult: LabelByPeriods[];
  isUserMediaLoading = false;
  chartImage: string;

  activeRange: Range;

  showExistingVideos: boolean;
  showExistingAudio: boolean;
  userFile: any;

  signup = new FormGroup({
    // email: new FormControl(null, Validators.required),
    image: new FormControl(null, [Validators.required, requiredFileType('png')])
  });
  success = false;

  constructor( private http: HttpClient ) {
  }
  ngAfterViewInit(): void {
    // this.fileUploaderComponent.registerOnChange((file: File) => this.userMediaUrl = URL.createObjectURL(file))
  }


  submit() {
    this.success = false;
    // if ( !this.signup.valid ) {
    //   markAllAsDirty(this.signup);
    //   return;
    // }

    console.log(this.signup.value.image);

    this.isUserMediaLoading = true;
    this.http.post('/upload-avatar', toFormData(this.signup.value), {
      reportProgress: true,
      observe: 'events',
      headers: {'enctype': 'multipart/form-data'}
    }).pipe(
      tap(p => console.log(p)),
      uploadProgress(progress => (this.progress = progress)),
      toResponseBody()
    ).subscribe(res => {
      this.progress = 0;
      this.success = true;
      this.signup.reset();
      this.showUserMedia = true;
      console.log(res);

      const path = ((res as any).path as string).replace('\/', '\\');
      this.http.get('http://127.0.0.1:5000/process_audio?file_path=' + path)
      .subscribe((res2: {results: LabelByPeriods[], plot: any}) => {
        console.log(res2);
        res2.results.forEach(labelByPeriod => {
          labelByPeriod.ranges = labelByPeriod.ranges.map(range => {
            return {
              start: range.start / 1000,
              end: range.end / 1000,
              startAsMinutes: this.toMinutesString(range.start / 1000),
              endAsMinutes: this.toMinutesString(range.end / 1000)
            };
          });
        });
        this.userMediaResult = res2.results;
        this.chartImage = res2.plot['py/b64'];
        this.isUserMediaLoading = false;
      });
      // this.http.get('/process_audio', {
      //   params: {
      //     'file_path': ((res as any).path as string).replace('\/', '\\')
      //   }
      // }).subscribe(res2 => {
      //   console.log(res2);
      // });


    }, err => {
      console.log(err);
    });
  }

  saveUploadedFileUrl(url: string) {
    console.log(url);
    this.userMediaUrl = url;
  }

  setMediaTime(range: Range) {
    console.log("WAŻNE: ", range);
    this.activeRange = range;
  }

  hasError( field: string, error: string ) {
    const control = this.signup.get(field);
    return control.dirty && control.hasError(error);
  }

  useOurAudioClick() {
    this.showExistingAudio = true;
  }

  toMinutesString(seconds: number) {
    const minutes = Math.floor(seconds / 60);
    const restOfSeconds = (seconds - minutes * 60)
    return `${minutes.toString().padStart(2, '0')}.${restOfSeconds.toString().padStart(2, '0')}`;
  }
}

export function markAllAsDirty( form: FormGroup ) {
  for ( const control of Object.keys(form.controls) ) {
    form.controls[control].markAsDirty();
  }
}

export function toFormData<T>( formValue: T ) {
  const formData = new FormData();

  for ( const key of Object.keys(formValue) ) {
    const value = formValue[key];
    formData.append(key, value);
  }
  console.log(formData);
  return formData;
}
