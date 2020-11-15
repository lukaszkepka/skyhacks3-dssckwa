import { Component, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

export interface Range {
  start: number;
  end: number;
  startAsMinutes?: string;
  endAsMinutes?: string;
}

export interface LabelByPeriods {
  label: string;
  ranges: Range[];
}

@Component({
  selector: 'app-audio',
  templateUrl: './audio.component.html',
  styleUrls: ['./audio.component.css']
})
export class AudioComponent implements OnInit {
  @Input() filePath: string;
  @Input() range: Range;

  constructor(private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
    console.log(this.filePath);
  }

  toMinutes(seconds: number) {
    const minutes = Math.floor(seconds / 60);
    const restOfSeconds = seconds - minutes * 60;
    return `${minutes}.${restOfSeconds}`;
  }

  sanitize(url: string) {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }
}
