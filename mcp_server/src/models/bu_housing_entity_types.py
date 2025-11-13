"""Custom entity type definitions for Boston University Housing Knowledge Graph.

This module defines entity types aligned with Common Core Ontology (CCO) terminology
for better interoperability and semantic consistency.

CCO Alignment:
- Person (Student, Staff) → cco:Person
- Facility (HousingFacility, ResidentialFacility, AmenityFacility) → cco:Facility
- Agreement (LeaseAgreement) → cco:Agreement
- ServiceRequest (MaintenanceRequest) → cco:ServiceRequest (Information Content Entity)
- Assignment (RoomAssignment) → cco:Directive (Information Content Entity)
- Policy (HousingPolicy) → cco:Policy (Directive Information Content Entity)
- Application (HousingApplication) → cco:Application (Information Content Entity)
- Event (HousingEvent) → cco:Act
- FinancialTransaction (Payment) → cco:Act
"""

from pydantic import BaseModel, Field


class Person(BaseModel):
    """A Person represents an individual in the BU Housing context (students, staff, residents).

    CCO Alignment: cco:Person - A Human Being
    Domain Context: Student or Staff member in BU Housing system

    Instructions for identifying and extracting persons:
    1. Look for mentions of students, residents, staff, tenants, or occupants
    2. Extract person names, IDs (BU ID, employee ID), email addresses when mentioned
    3. Identify role (student, staff, RA, RD, maintenance, etc.)
    4. For students: Capture status (undergraduate, graduate, international, etc.)
    5. For students: Note year/class level (freshman, sophomore, junior, senior, grad)
    6. For staff: Note position, department, responsibilities
    7. Track special needs, accommodations, or preferences
    8. Include contact information if provided
    9. Capture organizational affiliation (academic program, department, etc.)
    """

    name: str = Field(
        ...,
        description='Full name of the person',
    )
    person_id: str | None = Field(
        None,
        description='Unique identifier (BU ID, employee ID, etc.)',
    )
    role: str | None = Field(
        None,
        description='Role in housing context (student, RA, staff, resident, etc.)',
    )
    status: str | None = Field(
        None,
        description='Status (undergraduate, graduate, international, full-time staff, etc.)',
    )
    affiliation: str | None = Field(
        None,
        description='Organizational affiliation (academic program, department, school, etc.)',
    )
    contact_info: str | None = Field(
        None,
        description='Contact information (email, phone, office location) if mentioned',
    )


class ResidentialFacility(BaseModel):
    """A ResidentialFacility represents a specific living space (room, suite, apartment) within BU Housing.

    CCO Alignment: cco:Facility - A Site that has been designed to support habitation
    Domain Context: Individual housing unit where students reside

    Instructions for identifying and extracting housing units:
    1. Look for room numbers, suite numbers, or apartment identifiers
    2. Identify unit type (single, double, triple, quad, suite, apartment)
    3. Extract capacity information (number of beds, occupants)
    4. Note features (private bathroom, kitchen, balcony, etc.)
    5. Capture floor level and location within building
    6. Include accessibility features if mentioned
    7. Track furniture and furnishings provided
    8. Note condition or renovation status
    9. Identify any special designations (quiet floor, substance-free, etc.)
    """

    unit_number: str = Field(
        ...,
        description='Room, suite, or apartment number/identifier',
    )
    building_name: str = Field(
        ...,
        description='Name of the building where this unit is located',
    )
    unit_type: str | None = Field(
        None,
        description='Type of unit (single, double, triple, suite, apartment, etc.)',
    )
    capacity: int | None = Field(
        None,
        description='Maximum number of occupants',
    )
    features: str | None = Field(
        None,
        description='Notable features or amenities of the unit',
    )
    floor_level: str | None = Field(
        None,
        description='Floor number or level',
    )


class Facility(BaseModel):
    """A Facility represents a residence hall or housing building at Boston University.

    CCO Alignment: cco:Facility - A Site that has been designed to support some particular Processual Entity
    Domain Context: Residence hall, dormitory building, or housing complex

    Instructions for identifying and extracting facilities:
    1. Look for residence hall names (Warren Towers, West Campus, etc.)
    2. Identify building location/address on campus
    3. Extract building type (traditional dorm, apartment-style, brownstone)
    4. Note total capacity or number of units
    5. Identify amenities (dining hall, gym, study lounges, laundry)
    6. Capture special characteristics (honors housing, LLC, themed communities)
    7. Track accessibility features and accommodations
    8. Note proximity to campus facilities
    9. Include year built or renovation information if mentioned
    """

    name: str = Field(
        ...,
        description='Name of the residence hall or building',
    )
    location: str | None = Field(
        None,
        description='Campus location or address',
    )
    building_type: str | None = Field(
        None,
        description='Type of housing (traditional dorm, apartment-style, brownstone, etc.)',
    )
    total_capacity: int | None = Field(
        None,
        description='Total number of residents the building can house',
    )
    amenities: str | None = Field(
        None,
        description='Building amenities and facilities',
    )
    special_designation: str | None = Field(
        None,
        description='Special housing designation (honors, LLC, themed community, etc.)',
    )


class Agreement(BaseModel):
    """An Agreement represents a housing contract or lease between BU Housing and a student.

    CCO Alignment: cco:Agreement - A Directive Information Content Entity that prescribes mutual commitments
    Domain Context: Housing lease, contract, or housing agreement

    Instructions for identifying and extracting agreements:
    1. Look for contract terms, housing agreements, or lease mentions
    2. Extract start and end dates (academic year, semester, summer)
    3. Identify payment terms and amounts
    4. Note contract type (academic year, semester, summer, year-round)
    5. Capture any special terms or conditions
    6. Track contract status (active, pending, cancelled, completed)
    7. Include cancellation policy details if mentioned
    8. Note any deposits or fees required
    9. Identify housing assignment tied to the lease
    """

    contract_id: str | None = Field(
        None,
        description='Unique identifier for the lease/contract',
    )
    contract_type: str = Field(
        ...,
        description='Type of lease (academic year, semester, summer, year-round)',
    )
    start_date: str | None = Field(
        None,
        description='Lease start date',
    )
    end_date: str | None = Field(
        None,
        description='Lease end date',
    )
    payment_amount: str | None = Field(
        None,
        description='Total payment amount or rent',
    )
    terms: str | None = Field(
        None,
        description='Special terms, conditions, or policies of the lease',
    )
    status: str | None = Field(
        None,
        description='Contract status (active, pending, cancelled, completed)',
    )


class ServiceRequest(BaseModel):
    """A ServiceRequest represents a work order, repair request, or service ticket for housing facilities.

    CCO Alignment: cco:Information Content Entity - An entity that encodes information about a requested service
    Domain Context: Maintenance request, repair ticket, work order, or service request

    Instructions for identifying and extracting service requests:
    1. Look for mentions of repairs, fixes, work orders, or maintenance needs
    2. Extract request ID or ticket number if provided
    3. Identify the issue type (plumbing, electrical, HVAC, appliance, etc.)
    4. Capture priority level (emergency, urgent, routine)
    5. Note location (building, unit number) where work is needed
    6. Track status (submitted, in progress, completed, cancelled)
    7. Include submitter information if mentioned
    8. Note any deadline or completion date
    9. Capture resolution details when work is completed
    """

    request_id: str | None = Field(
        None,
        description='Unique identifier for the maintenance request',
    )
    issue_type: str = Field(
        ...,
        description='Type of maintenance issue (plumbing, electrical, HVAC, etc.)',
    )
    description: str = Field(
        ...,
        description='Detailed description of the maintenance issue',
    )
    priority: str | None = Field(
        None,
        description='Priority level (emergency, urgent, routine)',
    )
    location: str = Field(
        ...,
        description='Building and unit where maintenance is needed',
    )
    status: str | None = Field(
        None,
        description='Current status (submitted, in progress, completed, cancelled)',
    )
    submitted_date: str | None = Field(
        None,
        description='Date the request was submitted',
    )


class AmenityFacility(BaseModel):
    """An AmenityFacility represents a facility, service location, or shared resource available to BU Housing residents.

    CCO Alignment: cco:Facility - A Site designed to provide amenities or services
    Domain Context: Gym, laundry room, study lounge, mail room, or other shared facilities

    Instructions for identifying and extracting amenity facilities:
    1. Look for mentions of facilities (gym, laundry, study rooms, lounges)
    2. Identify services (mail room, package pickup, bike storage)
    3. Extract location (building-specific or shared across campus)
    4. Note access requirements or restrictions
    5. Capture hours of operation if mentioned
    6. Track capacity or availability
    7. Include any fees or costs associated with use
    8. Note amenity condition or recent updates
    9. Identify popular or highly-used amenities
    """

    name: str = Field(
        ...,
        description='Name of the amenity or facility',
    )
    amenity_type: str = Field(
        ...,
        description='Type of amenity (gym, laundry, study room, lounge, parking, etc.)',
    )
    location: str = Field(
        ...,
        description='Building or location where amenity is available',
    )
    access_details: str | None = Field(
        None,
        description='Access requirements, hours, or restrictions',
    )
    features: str | None = Field(
        None,
        description='Specific features or equipment available',
    )


class Assignment(BaseModel):
    """An Assignment represents the allocation of a person to a specific housing unit.

    CCO Alignment: cco:Directive Information Content Entity - An ICE prescribing an allocation or assignment
    Domain Context: Room assignment, housing placement, or unit allocation

    Instructions for identifying and extracting assignments:
    1. Look for mentions of student placements or room allocations
    2. Extract assignment dates (move-in, move-out dates)
    3. Identify bed space or specific location within unit
    4. Note roommate information if multiple occupants
    5. Track assignment status (confirmed, pending, waitlisted)
    6. Capture any special requests or accommodations
    7. Include lottery numbers or priority rankings
    8. Note assignment method (lottery, squatting, preference)
    9. Track changes or reassignments with reasons
    """

    person_name: str = Field(
        ...,
        description='Name of the person being assigned',
    )
    unit_number: str = Field(
        ...,
        description='Room/unit number being assigned',
    )
    building_name: str = Field(
        ...,
        description='Building where the assignment is located',
    )
    assignment_period: str = Field(
        ...,
        description='Time period for the assignment (Fall 2024, Spring 2025, etc.)',
    )
    move_in_date: str | None = Field(
        None,
        description='Scheduled move-in date',
    )
    move_out_date: str | None = Field(
        None,
        description='Scheduled move-out date',
    )
    status: str | None = Field(
        None,
        description='Assignment status (confirmed, pending, waitlisted, cancelled)',
    )


class Policy(BaseModel):
    """A Policy represents rules, regulations, or guidelines for BU Housing residents.

    CCO Alignment: cco:Policy - A Directive Information Content Entity that prescribes actions or behaviors
    Domain Context: Housing rules, regulations, conduct codes, or guidelines

    Instructions for identifying and extracting policies:
    1. Look for mentions of rules, regulations, or guidelines
    2. Identify policy categories (guests, quiet hours, pets, smoking, etc.)
    3. Extract specific requirements or restrictions
    4. Note consequences or penalties for violations
    5. Capture effective dates or policy changes
    6. Include any exceptions or special circumstances
    7. Track policy enforcement methods
    8. Note which buildings or residents are affected
    9. Identify safety policies and emergency procedures
    """

    policy_name: str = Field(
        ...,
        description='Name or title of the policy',
    )
    category: str = Field(
        ...,
        description='Policy category (guests, quiet hours, pets, alcohol, safety, etc.)',
    )
    description: str = Field(
        ...,
        description='Detailed description of the policy rules and requirements',
    )
    applies_to: str | None = Field(
        None,
        description='Who or what the policy applies to (all residents, specific buildings, etc.)',
    )
    consequences: str | None = Field(
        None,
        description='Consequences or penalties for policy violations',
    )


class Application(BaseModel):
    """An Application represents a student's application for BU Housing.

    CCO Alignment: cco:Information Content Entity - An ICE that encodes an application or request
    Domain Context: Housing application, lottery submission, or housing request

    Instructions for identifying and extracting applications:
    1. Look for mentions of housing applications or lottery participation
    2. Extract application ID or confirmation number
    3. Identify application type (new student, returning, transfer)
    4. Capture housing preferences ranked in order
    5. Note roommate requests or preferences
    6. Track application status and timeline
    7. Include special needs or accommodation requests
    8. Note lottery number or priority ranking
    9. Identify any deposits paid or required
    """

    application_id: str | None = Field(
        None,
        description='Unique application identifier',
    )
    applicant_name: str = Field(
        ...,
        description='Name of the student applying',
    )
    application_type: str = Field(
        ...,
        description='Type of application (new student, returning, transfer, etc.)',
    )
    preferences: str = Field(
        ...,
        description='Housing preferences in ranked order',
    )
    roommate_requests: str | None = Field(
        None,
        description='Requested roommates or roommate preferences',
    )
    status: str | None = Field(
        None,
        description='Application status (submitted, under review, approved, denied, waitlisted)',
    )
    submission_date: str | None = Field(
        None,
        description='Date the application was submitted',
    )


class Event(BaseModel):
    """An Event represents activities, inspections, or occurrences in BU Housing.

    CCO Alignment: cco:Act - A Processual Entity performed by an Agent
    Domain Context: Housing events, inspections, incidents, or scheduled activities

    Instructions for identifying and extracting events:
    1. Look for scheduled events (move-in day, orientation, community events)
    2. Identify inspections (room checks, fire safety, move-out inspections)
    3. Extract incident reports or violations
    4. Note building closures or maintenance windows
    5. Capture event date, time, and location
    6. Track attendance or participation requirements
    7. Include event purpose and expected outcomes
    8. Note any follow-up actions required
    9. Identify mandatory vs. optional events
    """

    event_name: str = Field(
        ...,
        description='Name or title of the event',
    )
    event_type: str = Field(
        ...,
        description='Type of event (move-in, inspection, community event, incident, etc.)',
    )
    date: str | None = Field(
        None,
        description='Date and time of the event',
    )
    location: str = Field(
        ...,
        description='Building or specific location of the event',
    )
    description: str = Field(
        ...,
        description='Detailed description of the event',
    )
    mandatory: bool | None = Field(
        None,
        description='Whether attendance is mandatory',
    )


class FinancialTransaction(BaseModel):
    """A FinancialTransaction represents financial transactions and payments related to BU Housing.

    CCO Alignment: cco:Act - A Processual Entity involving exchange of money
    Domain Context: Rent payments, deposits, fees, refunds, or housing-related charges

    Instructions for identifying and extracting financial transactions:
    1. Look for mentions of rent payments, housing fees, or charges
    2. Extract payment amounts and currency
    3. Identify payment type (rent, deposit, damage fee, late fee, etc.)
    4. Capture payment date and due date
    5. Note payment method (bursar account, credit card, check, etc.)
    6. Track payment status (pending, completed, overdue, refunded)
    7. Include receipt or transaction numbers
    8. Note any payment plans or installment arrangements
    9. Identify refunds or credits when applicable
    """

    payment_id: str | None = Field(
        None,
        description='Unique payment or transaction identifier',
    )
    amount: str = Field(
        ...,
        description='Payment amount',
    )
    payment_type: str = Field(
        ...,
        description='Type of payment (rent, deposit, damage fee, late fee, etc.)',
    )
    due_date: str | None = Field(
        None,
        description='Payment due date',
    )
    payment_date: str | None = Field(
        None,
        description='Date payment was made',
    )
    status: str | None = Field(
        None,
        description='Payment status (pending, completed, overdue, refunded)',
    )
    payer_name: str = Field(
        ...,
        description='Name of the student making the payment',
    )


# Registry of all BU Housing entity types (CCO-aligned)
BU_HOUSING_ENTITY_TYPES: dict[str, type[BaseModel]] = {
    'Person': Person,  # Covers students, staff, residents
    'ResidentialFacility': ResidentialFacility,  # Individual housing units
    'Facility': Facility,  # Buildings and residence halls
    'Agreement': Agreement,  # Leases and housing contracts
    'ServiceRequest': ServiceRequest,  # Maintenance and service requests
    'AmenityFacility': AmenityFacility,  # Shared facilities and amenities
    'Assignment': Assignment,  # Room assignments and allocations
    'Policy': Policy,  # Housing policies and regulations
    'Application': Application,  # Housing applications
    'Event': Event,  # Housing events and occurrences
    'FinancialTransaction': FinancialTransaction,  # Payments and financial transactions
}
