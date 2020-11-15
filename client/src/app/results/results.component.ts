import { Component, Input, OnInit, Output } from '@angular/core';
import { EventEmitter } from '@angular/core';
import { LabelByPeriods } from '../audio/audio.component';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {
  @Output() periodClickEvent: EventEmitter<Range> = new EventEmitter<Range>();
  @Input() labelsByPeriods: LabelByPeriods[];
  constructor() { }

  ngOnInit(): void {
  }

  periodClicked(range: Range) {
    this.periodClickEvent.emit(range);
  }

}
