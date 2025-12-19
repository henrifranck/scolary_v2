import { useEffect, useMemo, useState, type ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  GraduationCap,
  BookOpen,
  Calendar,
  Filter,
  Eye,
  EyeOff
} from "lucide-react";

import { cn } from "../../lib/utils";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "../ui/select";
import { Tabs, TabsList, TabsTrigger } from "../ui/tabs";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import {
  fetchMentions as fetchMentionOptions,
  fetchJourneys as fetchJourneyOptions,
  fetchCollegeYears
} from "../../services/inscription-service";

export interface MentionOption {
  id: string;
  label: string;
}

export interface JourneyOption {
  id: string;
  label: string;
  id_mention?: string;
  mentionId?: string;
  semesterList?: string[];
}

export interface AcademicYearOption {
  id: string;
  label: string;
}

export interface AcademicFilterValue {
  id_mention: string;
  id_journey: string;
  semester: string;
  id_year: string;
}

const getJourneyMentionId = (journey: JourneyOption) =>
  journey.id_mention ?? journey.mentionId ?? "";

interface AcademicFiltersProps {
  value: AcademicFilterValue;
  onChange: (value: AcademicFilterValue) => void;
  mentionOptions?: MentionOption[];
  journeyOptions?: JourneyOption[];
  academicYearOptions?: AcademicYearOption[];
  semesters: string[];
  className?: string;
  summarySlot?: ReactNode;
  showResetButton?: boolean;
  showActiveFilters?: boolean;
  journeysLoading?: boolean;
  collapsed?: boolean;
  onCollapsedChange?: (collapsed: boolean) => void;
}

export const AcademicFilters = ({
  value,
  onChange,
  mentionOptions: mentionOptionsProp = [],
  journeyOptions: journeyOptionsProp = [],
  academicYearOptions: academicYearOptionsProp = [],
  semesters,
  className,
  summarySlot,
  showResetButton = true,
  showActiveFilters = true,
  journeysLoading: journeysLoadingProp = false,
  collapsed: collapsedProp,
  onCollapsedChange
}: AcademicFiltersProps) => {
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const isCollapsedControlled = collapsedProp !== undefined;
  const collapsed = isCollapsedControlled ? collapsedProp : internalCollapsed;
  const setCollapsed = (next: boolean) => {
    if (!isCollapsedControlled) {
      setInternalCollapsed(next);
    }
    onCollapsedChange?.(next);
  };
  const shouldFetchMentions = mentionOptionsProp.length === 0;
  const { data: fetchedMentions = [], isFetching: mentionsFetching } = useQuery(
    {
      queryKey: ["academic-filters", "mentions"],
      queryFn: fetchMentionOptions,
      enabled: shouldFetchMentions
    }
  );

  const resolvedMentionOptions = useMemo<MentionOption[]>(
    () =>
      mentionOptionsProp.length
        ? mentionOptionsProp
        : fetchedMentions.map((mention) => ({
            id: String(mention.id),
            label:
              mention.name?.trim() ||
              mention.abbreviation?.trim() ||
              `Mention ${mention.id}`
          })),
    [mentionOptionsProp, fetchedMentions]
  );

  const shouldFetchAcademicYears = academicYearOptionsProp.length === 0;
  const { data: fetchedAcademicYears = [], isFetching: academicYearsFetching } =
    useQuery({
      queryKey: ["academic-filters", "academic-years"],
      queryFn: fetchCollegeYears,
      enabled: shouldFetchAcademicYears
    });

  const resolvedAcademicYearOptions = useMemo<AcademicYearOption[]>(
    () =>
      academicYearOptionsProp.length
        ? academicYearOptionsProp
        : fetchedAcademicYears.map((year) => ({
            id: String(year.id),
            label: year.name ?? `Year ${year.id}`
          })),
    [academicYearOptionsProp, fetchedAcademicYears]
  );

  const shouldFetchJourneys = journeyOptionsProp.length === 0;
  const {
    data: fetchedJourneys = [],
    isFetching: autoJourneysFetching,
    isPending: autoJourneysPending
  } = useQuery({
    queryKey: ["academic-filters", "journeys", value.id_mention],
    queryFn: () => fetchJourneyOptions(value.id_mention),
    enabled: shouldFetchJourneys && Boolean(value.id_mention)
  });

  const resolvedJourneyOptions = useMemo<JourneyOption[]>(
    () =>
      journeyOptionsProp.length
        ? journeyOptionsProp
        : fetchedJourneys.map((journey) => {
            const mentionId =
              journey.id_mention !== undefined
                ? journey.id_mention
                : value.id_mention;

            const normalized = mentionId ? String(mentionId) : value.id_mention;
            const semesterList = Array.isArray(journey.semester_list)
              ? journey.semester_list
                  .map((entry) =>
                    typeof entry === "string"
                      ? entry
                      : (entry?.semester ?? null)
                  )
                  .filter((semester): semester is string => Boolean(semester))
              : [];

            return {
              id: String(journey.id),
              label:
                journey.name ?? journey.abbreviation ?? `Journey ${journey.id}`,
              id_mention: normalized,
              mentionId: normalized,
              semesterList
            };
          }),
    [journeyOptionsProp, fetchedJourneys, value.id_mention]
  );

  const resolvedJourneysLoading =
    journeysLoadingProp ||
    (shouldFetchJourneys && (autoJourneysFetching || autoJourneysPending));

  const availableJourneys = useMemo(
    () =>
      resolvedJourneyOptions.filter(
        (journey) => getJourneyMentionId(journey) === value.id_mention
      ),
    [resolvedJourneyOptions, value.id_mention]
  );

  const selectedJourney = availableJourneys.find(
    (journey) => journey.id === value.id_journey
  );
  const allowedSemesters = selectedJourney?.semesterList?.length
    ? selectedJourney.semesterList
    : [];

  useEffect(() => {
    const hasJourney = availableJourneys.some(
      (journey) => journey.id === value.id_journey
    );

    if (!availableJourneys.length && value.id_journey) {
      onChange({
        ...value,
        id_journey: ""
      });
      return;
    }

    if (value.id_journey && !hasJourney) {
      onChange({
        ...value,
        id_journey: ""
      });
    }
  }, [availableJourneys, onChange, value]);

  const handleMentionChange = (id_mention: string) => {
    const nextJourneys = resolvedJourneyOptions.filter(
      (journey) => getJourneyMentionId(journey) === id_mention
    );
    const resolvedJourneyId = nextJourneys.some(
      (journey) => journey.id === value.id_journey
    )
      ? value.id_journey
      : "";
    const nextSelectedJourney = nextJourneys.find(
      (journey) => journey.id === resolvedJourneyId
    );
    const journeySemesters =
      nextSelectedJourney?.semesterList?.length && semesters.length
        ? nextSelectedJourney.semesterList
        : semesters;
    const resolvedSemester = journeySemesters.includes(value.semester)
      ? value.semester
      : (journeySemesters[0] ?? "");

    onChange({
      ...value,
      id_mention,
      id_journey: resolvedJourneyId,
      semester: resolvedSemester
    });
  };

  const handleJourneyChange = (id_journey: string) => {
    const nextJourney = availableJourneys.find(
      (journey) => journey.id === id_journey
    );
    const journeySemesters =
      nextJourney?.semesterList?.length && semesters.length
        ? nextJourney.semesterList
        : semesters;
    const resolvedSemester = journeySemesters.includes(value.semester)
      ? value.semester
      : (journeySemesters[0] ?? "");

    onChange({
      ...value,
      id_journey,
      semester: resolvedSemester
    });
  };

  const handleYearChange = (id_year: string) => {
    onChange({
      ...value,
      id_year
    });
  };

  const handleSemesterChange = (semester: string) => {
    onChange({
      ...value,
      semester
    });
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (value.id_mention) count++;
    if (value.id_journey) count++;
    if (value.semester) count++;
    if (value.id_year) count++;
    return count;
  };

  const getSelectedMentionLabel = () => {
    return (
      resolvedMentionOptions.find((m) => m.id === value.id_mention)?.label || ""
    );
  };

  const getSelectedJourneyLabel = () => {
    return (
      availableJourneys.find((j) => j.id === value.id_journey)?.label || ""
    );
  };

  const getSelectedYearLabel = () => {
    return (
      resolvedAcademicYearOptions.find((y) => y.id === value.id_year)?.label ||
      ""
    );
  };

  const mentionPlaceholder =
    shouldFetchMentions && mentionsFetching
      ? "Loading mentions..."
      : "Select mention";

  const academicYearPlaceholder =
    shouldFetchAcademicYears && academicYearsFetching
      ? "Loading years..."
      : "Select year";

  const journeyPlaceholder = resolvedJourneysLoading
    ? "Loading journeys..."
    : value.id_mention
      ? availableJourneys.length
        ? "Select journey"
        : "No journey available"
      : "Select mention first";

  return (
    <div className={cn("space-y-6", className)}>
      {/* Header with filter count and reset button */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold">Academic Filters</h3>
          </div>
          {showActiveFilters && getActiveFiltersCount() > 0 && (
            <Badge variant="secondary" className="gap-1">
              {getActiveFiltersCount()} active
            </Badge>
          )}
        </div>
        {showResetButton && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCollapsed(!collapsed)}
            className="gap-2"
          >
            {collapsed ? (
              <>
                <Eye className="h-4 w-4" />
                Show filters
              </>
            ) : (
              <>
                <EyeOff className="h-4 w-4" />
                Hide filters
              </>
            )}
          </Button>
        )}
      </div>

      {!collapsed && (
        <>
          {/* Active filters display */}
          {showActiveFilters && getActiveFiltersCount() > 0 && (
            <div className="flex flex-wrap gap-2">
              {getSelectedMentionLabel() && (
                <Badge variant="outline" className="gap-1">
                  <GraduationCap className="h-3 w-3" />
                  {getSelectedMentionLabel()}
                </Badge>
              )}
              {getSelectedJourneyLabel() && (
                <Badge variant="outline" className="gap-1">
                  <BookOpen className="h-3 w-3" />
                  {getSelectedJourneyLabel()}
                </Badge>
              )}
              {getSelectedYearLabel() && (
                <Badge variant="outline" className="gap-1">
                  <Calendar className="h-3 w-3" />
                  {getSelectedYearLabel()}
                </Badge>
              )}
              {value.semester && (
                <Badge variant="outline" className="gap-1">
                  <BookOpen className="h-3 w-3" />
                  {value.semester}
                </Badge>
              )}
            </div>
          )}

          {/* Filter controls */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Mention Selection */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-muted-foreground" />
                <label className="text-sm font-medium">Mention</label>
              </div>
              <Select
                value={value.id_mention}
                onValueChange={handleMentionChange}
              >
                <SelectTrigger className="h-11">
                  <SelectValue placeholder={mentionPlaceholder} />
                </SelectTrigger>
                <SelectContent>
                  {resolvedMentionOptions.map((mention) => (
                    <SelectItem key={mention.id} value={mention.id}>
                      <div className="flex items-center gap-2">
                        <GraduationCap className="h-4 w-4 text-muted-foreground" />
                        {mention.label}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Journey Selection */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-muted-foreground" />
                <label className="text-sm font-medium">Journey</label>
              </div>
              <Select
                value={value.id_journey}
                onValueChange={handleJourneyChange}
                disabled={!availableJourneys.length || resolvedJourneysLoading}
              >
                <SelectTrigger className="h-11">
                  <SelectValue placeholder={journeyPlaceholder} />
                </SelectTrigger>
                <SelectContent>
                  {availableJourneys.length ? (
                    availableJourneys.map((journey) => (
                      <SelectItem key={journey.id} value={journey.id}>
                        <div className="flex items-center gap-2">
                          <BookOpen className="h-4 w-4 text-muted-foreground" />
                          {journey.label}
                        </div>
                      </SelectItem>
                    ))
                  ) : (
                    <SelectItem value="__no_journey" disabled>
                      No journey available
                    </SelectItem>
                  )}
                </SelectContent>
              </Select>
            </div>

            {/* Academic Year Selection */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <label className="text-sm font-medium">Academic Year</label>
              </div>
              <Select
                value={value.id_year}
                onValueChange={handleYearChange}
                disabled={!resolvedAcademicYearOptions.length}
              >
                <SelectTrigger className="h-11">
                  <SelectValue
                    placeholder={
                      resolvedAcademicYearOptions.length
                        ? academicYearPlaceholder
                        : "No year available"
                    }
                  />
                </SelectTrigger>
                <SelectContent>
                  {resolvedAcademicYearOptions.length ? (
                    resolvedAcademicYearOptions.map((year) => (
                      <SelectItem key={year.id} value={year.id}>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4 text-muted-foreground" />
                          {year.label}
                        </div>
                      </SelectItem>
                    ))
                  ) : (
                    <SelectItem value="__no_year" disabled>
                      No year available
                    </SelectItem>
                  )}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Semester Selection */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-muted-foreground" />
              <label className="text-sm font-medium">Semester</label>
            </div>
            <Tabs
              value={value.semester}
              onValueChange={handleSemesterChange}
              className="w-full"
            >
              <TabsList className="grid w-full grid-cols-5 lg:grid-cols-10 gap-1 bg-muted p-1">
                {semesters.map((semester) => (
                  <TabsTrigger
                    key={semester}
                    value={semester}
                    className={cn(
                      "text-xs data-[state=active]:bg-background data-[state=active]:shadow-sm",
                      !allowedSemesters.includes(semester) &&
                        "opacity-50 pointer-events-none cursor-not-allowed"
                    )}
                    disabled={!allowedSemesters.includes(semester)}
                  >
                    {semester}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
          </div>

          {/* Summary Slot */}
          {summarySlot && <div className="pt-4 border-t">{summarySlot}</div>}
        </>
      )}
    </div>
  );
};
