import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExistingResourcePickerComponent } from './existing-resource-picker.component';

describe('ExistingResourcePickerComponent', () => {
  let component: ExistingResourcePickerComponent;
  let fixture: ComponentFixture<ExistingResourcePickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExistingResourcePickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExistingResourcePickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
