from django.shortcuts import render

from .utils.resume_parser import extract_text_from_resume
from .utils.similarity import calculate_similarity
from .utils.candidate_info import extract_candidate_info
from .utils.skills import extract_skills


def home(request):

    # -----------------------------------------
    # GET REQUEST
    # -----------------------------------------

    if request.method == "GET":

        return render(
            request,
            "screening/home.html"
        )


    # -----------------------------------------
    # POST REQUEST
    # -----------------------------------------

    if request.method == "POST":

        # Get uploaded resumes
        resumes = request.FILES.getlist("resumes")

        # Get job description
        job_description = request.POST.get(
            "job_description",
            ""
        ).strip()


        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not resumes:

            return render(
                request,
                "screening/home.html",
                {
                    "error": "Please upload at least one resume."
                }
            )


        if not job_description:

            return render(
                request,
                "screening/home.html",
                {
                    "error": "Please enter a job description."
                }
            )


        # -----------------------------------------
        # EXTRACT JOB SKILLS
        # -----------------------------------------

        job_skills = extract_skills(
            job_description
        )


        if not job_skills:

            return render(
                request,
                "screening/home.html",
                {
                    "error": (
                        "No predefined skills detected. "
                        "Please include skills such as "
                        "Python, Django, SQL, JavaScript, "
                        "HTML, CSS, Git, etc."
                    )
                }
            )


        # List for storing results
        results = []


        # -----------------------------------------
        # PROCESS EACH RESUME
        # -----------------------------------------

        for resume in resumes:

            try:

                # ---------------------------------
                # EXTRACT RESUME TEXT
                # ---------------------------------

                resume_text = extract_text_from_resume(
                    resume
                )


                if not resume_text.strip():

                    continue


                # ---------------------------------
                # ML SIMILARITY
                # ---------------------------------

                similarity_score = calculate_similarity(
                    resume_text,
                    job_description
                )


                # ---------------------------------
                # EXTRACT RESUME SKILLS
                # ---------------------------------

                resume_skills = extract_skills(
                    resume_text
                )


                # ---------------------------------
                # MATCHED SKILLS
                # ---------------------------------

                matching_skills = sorted(
                    set(job_skills).intersection(
                        set(resume_skills)
                    )
                )


                # ---------------------------------
                # MISSING SKILLS
                # ---------------------------------

                missing_skills = sorted(
                    set(job_skills).difference(
                        set(resume_skills)
                    )
                )


                # ---------------------------------
                # SKILL SCORE
                # ---------------------------------

                if len(job_skills) > 0:

                    skill_score = round(
                        (
                            len(matching_skills)
                            /
                            len(job_skills)
                        )
                        * 100,
                        2
                    )

                else:

                    skill_score = 0


                # ---------------------------------
                # FINAL SCORE
                # ---------------------------------

                final_score = round(
                    (
                        similarity_score * 0.60
                    )
                    +
                    (
                        skill_score * 0.40
                    ),
                    2
                )


                # ---------------------------------
                # STATUS
                # ---------------------------------

                if final_score >= 75:

                    status = "Strong Match"

                elif final_score >= 50:

                    status = "Moderate Match"

                else:

                    status = "Low Match"


                # ---------------------------------
                # CANDIDATE INFORMATION
                # ---------------------------------

                candidate_info = extract_candidate_info(
                    resume_text
                )


                # ---------------------------------
                # SCORE COMPONENTS
                # ---------------------------------

                similarity_contribution = round(
                    similarity_score * 0.60,
                    2
                )

                skill_contribution = round(
                    skill_score * 0.40,
                    2
                )


                # ---------------------------------
                # SCREENING SUMMARY
                # ---------------------------------

                if final_score >= 75:

                    summary = (
                        "The resume has strong alignment "
                        "with the job description based on "
                        "machine-learning text similarity "
                        "and detected technical skills."
                    )

                elif final_score >= 50:

                    summary = (
                        "The resume has moderate alignment "
                        "with the job description. The "
                        "candidate's detected skills match "
                        "the requirements, while the text "
                        "similarity score affects the overall "
                        "match score."
                    )

                else:

                    summary = (
                        "The resume has limited alignment "
                        "with the current job description "
                        "according to the screening criteria."
                    )


                # ---------------------------------
                # ADD RESULT
                # ---------------------------------

                results.append({

                    "filename": resume.name,

                    "name": candidate_info.get(
                        "name",
                        "Not detected"
                    ),

                    "email": candidate_info.get(
                        "email",
                        "Not detected"
                    ),

                    "phone": candidate_info.get(
                        "phone",
                        "Not detected"
                    ),

                    "similarity_score": similarity_score,

                    "skill_score": skill_score,

                    "final_score": final_score,

                    "similarity_contribution":
                        similarity_contribution,

                    "skill_contribution":
                        skill_contribution,

                    "status": status,

                    "matching_skills":
                        matching_skills,

                    "missing_skills":
                        missing_skills,

                    "summary": summary,

                    "matched_count":
                        len(matching_skills),

                    "required_count":
                        len(job_skills),

                })


            except Exception as e:

                print(
                    f"Error processing "
                    f"{resume.name}: {e}"
                )


        # -----------------------------------------
        # NO RESULTS
        # -----------------------------------------

        if not results:

            return render(
                request,
                "screening/home.html",
                {
                    "error": (
                        "Could not extract readable text "
                        "from the uploaded resume(s). "
                        "Please upload a PDF or DOCX file."
                    )
                }
            )


        # -----------------------------------------
        # SORT RESULTS
        # -----------------------------------------

        results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )


        # -----------------------------------------
        # ASSIGN RANK
        # -----------------------------------------

        for index, result in enumerate(
            results,
            start=1
        ):

            result["rank"] = index


        # -----------------------------------------
        # RESULTS PAGE
        # -----------------------------------------

        return render(
            request,
            "screening/results.html",
            {
                "results": results,

                "job_skills": job_skills,

                "job_skill_count":
                    len(job_skills),

                "resume_count":
                    len(results),
            }
        )