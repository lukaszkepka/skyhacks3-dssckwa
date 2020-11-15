import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-existing-resource-picker',
  templateUrl: './existing-resource-picker.component.html',
  styleUrls: ['./existing-resource-picker.component.css']
})
export class ExistingResourcePickerComponent implements OnInit {
  @Input() buttonName;
  constructor() { }

  ngOnInit(): void {
  }

}
